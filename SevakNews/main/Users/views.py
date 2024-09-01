from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.db.models import F, Count
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from app.models import NewsBase, NewsCategory, CommentsBase
from .user_models import UserBase

from app.forms import DateFilterForm, CreateNewsForm, LeaveCommentForm
from .forms import UserRegistrationForm, UserLoginForm, UserInfoUpdateForm, \
                        SetUserNotificationForm, SendMassMailForm
                        
from .utils import send_email_for_verify


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            user.user_base.email_verify = True
            user.user_base.save()
            send_mail(f'Добро пожаловать на SevakNews',
                      f'Уважаемый {user.first_name} {user.last_name}\n\n'
                      f'Мы рады сообщить вам, что ваша регистрация на SevakNews успешно завершена. '
                      f'Теперь вы можете получить доступ ко всем функциям и эксклюзивному контенту, '
                      f'доступным на нашей платформе.',
                      'sevak.grigoryan.06@mail.ru',
                      [user.email])
            return HttpResponse('Ваша почта успешно подтверждена!')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uid64):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

def register(request):
    form = UserRegistrationForm()
    
    if 'button_1' in request.POST:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    send_email_for_verify(request=request, user=user)
                    messages.info(request, 'На вашу почту было отправлено письмо, подтвердите его, чтобы зайти на свой аккаунт')
                    return redirect('login')
                except Exception as _ex:
                    messages.error(request, _ex)
            else:
                messages.error(request, 'Ошибка регистрации!')

    return render(request, 'Users/sign_up.html', {'form': form, 'title': 'Регистрация'})


def user_login(request):
    form = UserLoginForm()
    form2 = UserInfoUpdateForm(instance=request.user if request.user.is_authenticated else None)

    if request.method == 'POST':
        if 'button_1' in request.POST:
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user.user_base.email_verify == True:
                    login(request, user)
                    messages.success(request, 'Добро пожаловать!')
                else:
                    messages.error(request, 'Вам нужно подтвердить почту')
                    
                return redirect('login')
            else:
                messages.error(request, 'Ошибка авторизации!')
                
        elif 'button_2' in request.POST:
            form2 = UserInfoUpdateForm(request.POST, request.FILES)
            if form2.is_valid():
                user = User.objects.get(username=request.user.username)
                if  form2.cleaned_data['first_name'] != '':
                    user.first_name = form2.cleaned_data['first_name']
                if form2.cleaned_data['last_name'] != '':
                    user.last_name = form2.cleaned_data['last_name']
                if 'photo' in request.FILES:
                    user = UserBase.objects.get(user__username=request.user.username)
                    user.photo = request.FILES['photo']
                user.save()
                messages.success(request, 'Ваш профиль успешно обновлен')
                return redirect(to='login')
            else:
                messages.error(request, 'Ошибка обновления')

    try:
        user_info = UserBase.objects.get(user__username=request.user.username)
        user_articles_id = UserBase.objects.values('GetAuthors').filter(user__username=request.user.username).order_by('GetAuthors')
        user_articles_cnt = UserBase.objects.values('GetAuthors').annotate(cnt=Count('GetAuthors')).filter(user__username=request.user.username).order_by('GetAuthors')
        cnt_articles = user_articles_cnt.first()['cnt']
        news = NewsBase.objects.filter(pk__in=user_articles_id).select_related()
    except UserBase.DoesNotExist:
        user_info = None
        cnt_articles = 0
        news = []

    return render(request, 'Users/login.html', {
        'form': form,
        'form2': form2,
        'title': 'Авторизация',
        'user_info': user_info,
        'cnt_articles': cnt_articles,
        'news': news,
    })
    
    
def user_logout(request):
    logout(request)
    return redirect(to='home')
    

def SendMassMailView(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SendMassMailForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['content'])
                users_emails = [item['email'] for item in list(User.objects.filter(user_base__notification=True).values('email'))]
                subject = form.cleaned_data['title']
                html_content = form.cleaned_data['content']
                text_content = strip_tags(html_content)  # Extract plain text from HTML content

                message = EmailMultiAlternatives(subject, text_content, 'sevak.grigoryan.06@mail.ru', users_emails)
                message.attach_alternative(html_content, "text/html")
                message.send(fail_silently=True)
        else:
            form = SendMassMailForm()
        
        return render(request, 'Users/send_mass_mail.html', {'form': form, 'title': 'Отправка массовых писем'})
    else:
        return HttpResponse('Эта страница доступна только суперпользователю')
    
    
def not_authenticated(request):
    messages.error(request, 'Чтобы прочитать новость нужно авторизаваться')
    return redirect('login')


class UserPage(ListView):
    model = UserBase
    template_name = 'Users/UserPage.html'
    context_object_name = 'user_info'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_articles_id = UserBase.objects.values(news=F('GetAuthors')).filter(user__username=self.kwargs['username'])
            authors_news = NewsBase.objects.filter(pk__in=user_articles_id)
            cnt_articles = len(user_articles_id) if list(user_articles_id)[0]['news'] != None else 0
        except:
            user_articles_id = None
            authors_news = None
            cnt_articles = 0
        
        context['title'] = self.kwargs['username']
        context['authors_news'] = authors_news
        context['cnt_articles'] = cnt_articles
        
        return context
    
    def get_queryset(self):
        return UserBase.objects.get(user__username=self.kwargs['username'])