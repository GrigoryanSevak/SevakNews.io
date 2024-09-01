from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.db.models import F
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import QueryDict
from django.utils import timezone
from django.core.paginator import Paginator

from .models import NewsBase, NewsCategory, CommentsBase
from Users.user_models import UserBase

from .forms import DateFilterForm, CreateNewsForm, LeaveCommentForm
from Users.forms import UserRegistrationForm, UserLoginForm, UserInfoUpdateForm, \
                        SetUserNotificationForm, SendMassMailForm                 

from .filters import DateFilter

class HomeNews(ListView):
    model = NewsBase
    template_name = 'app/home.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['form'] = DateFilterForm()
        context['filter'] = DateFilter()
        return context

    def get_queryset(self):
        return NewsBase.objects.filter(is_published=True).select_related('category')

    def post(self, request, *args, **kwargs):
        form = DateFilterForm(request.POST)
        filter = DateFilter(request.POST)
        if form.is_valid():
            data = form.cleaned_data['filter_date']
            views = form.cleaned_data['views']
            
            date_list = dict(filter.data.lists())
            
            try:
                created_at_min = date_list['created_at_after'][0]
                created_at_min = datetime.strptime(created_at_min, '%Y-%m-%d %H:%M')
                created_at_min_year = created_at_min.year
                created_at_min_month = created_at_min.month
                created_at_min_day = created_at_min.day
                created_at_min_hour = created_at_min.hour
                created_at_min_minute = created_at_min.minute
            except:
                created_at_min = ''
            
            try:
                created_at_max = date_list['created_at_before'][0]
                created_at_max = datetime.strptime(created_at_max, '%Y-%m-%d %H:%M')
                created_at_max_year = created_at_max.year
                created_at_max_month = created_at_max.month
                created_at_max_day = created_at_max.day
                created_at_max_hour = created_at_max.hour
                created_at_max_minute = created_at_max.minute
            except:
                created_at_max = ''
            
            today = datetime.today()
            news = NewsBase.objects.filter(is_published=True, views__lte=views).select_related('category')

            if created_at_min == '' and created_at_max == '':
                if data == 'today':
                    news = news.filter(created_at__date=today)
                elif data == 'yesterday':
                    news = news.filter(created_at__date=today - timedelta(days=1))
                elif data == 'day_before_yesterday':
                    news = news.filter(created_at__date=today - timedelta(days=2))
                elif data == 'all_days':
                    pass

            elif created_at_min != '' and created_at_max == '':
                min_date = timezone.make_aware(datetime(created_at_min_year, created_at_min_month, created_at_min_day, created_at_min_hour, created_at_min_minute), timezone.get_default_timezone())
                news = news.filter(created_at__gte=min_date)

            elif created_at_min == '' and created_at_max != '':
                max_date = timezone.make_aware(datetime(created_at_max_year, created_at_max_month, created_at_max_day, created_at_max_hour, created_at_max_minute), timezone.get_default_timezone())
                news = news.filter(created_at__lte=max_date)

            elif created_at_min != '' and created_at_max != '':
                min_date = timezone.make_aware(datetime(created_at_min_year, created_at_min_month, created_at_min_day, created_at_min_hour, created_at_min_minute), timezone.get_default_timezone())
                max_date = timezone.make_aware(datetime(created_at_max_year, created_at_max_month, created_at_max_day, created_at_max_hour, created_at_max_minute), timezone.get_default_timezone())
                news = news.filter(created_at__range=(min_date, max_date))
            
            
            return render(request, 'app/home.html', {'form': form, 'news': news, 'filter': filter})
        else:
            return render(request, 'app/home.html', {'form': form, 'filter': filter})
        
    
class CategoryNews(ListView):
    model = NewsBase
    template_name = 'app/category.html'
    context_object_name = 'news'
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']
        context['form'] = DateFilterForm()
        return context
    
    def get_queryset(self):
        return NewsBase.objects.filter(is_published = True, category__title=self.kwargs['title']).select_related('category')
    
    def post(self, request, *args, **kwargs):
        form = DateFilterForm(request.POST)
        filter = DateFilter(request.POST)
        if form.is_valid():
            data = form.cleaned_data['filter_date']
            views = form.cleaned_data['views']
            
            date_list = dict(filter.data.lists())
            
            try:
                created_at_min = date_list['created_at_after'][0]
                created_at_min = datetime.strptime(created_at_min, '%Y-%m-%d %H:%M')
                created_at_min_year = created_at_min.year
                created_at_min_month = created_at_min.month
                created_at_min_day = created_at_min.day
                created_at_min_hour = created_at_min.hour
                created_at_min_minute = created_at_min.minute
            except:
                created_at_min = ''
            
            try:
                created_at_max = date_list['created_at_before'][0]
                created_at_max = datetime.strptime(created_at_max, '%Y-%m-%d %H:%M')
                created_at_max_year = created_at_max.year
                created_at_max_month = created_at_max.month
                created_at_max_day = created_at_max.day
                created_at_max_hour = created_at_max.hour
                created_at_max_minute = created_at_max.minute
            except:
                created_at_max = ''
            
            today = datetime.today()
            news = NewsBase.objects.filter(is_published=True, views__lte=views, category__title=self.kwargs['title']).select_related('category')

            if created_at_min == '' and created_at_max == '':
                if data == 'today':
                    news = news.filter(created_at__date=today)
                elif data == 'yesterday':
                    news = news.filter(created_at__date=today - timedelta(days=1))
                elif data == 'day_before_yesterday':
                    news = news.filter(created_at__date=today - timedelta(days=2))
                elif data == 'all_days':
                    pass

            elif created_at_min != '' and created_at_max == '':
                min_date = timezone.make_aware(datetime(created_at_min_year, created_at_min_month, created_at_min_day, created_at_min_hour, created_at_min_minute), timezone.get_default_timezone())
                news = news.filter(created_at__gte=min_date)

            elif created_at_min == '' and created_at_max != '':
                max_date = timezone.make_aware(datetime(created_at_max_year, created_at_max_month, created_at_max_day, created_at_max_hour, created_at_max_minute), timezone.get_default_timezone())
                news = news.filter(created_at__lte=max_date)

            elif created_at_min != '' and created_at_max != '':
                min_date = timezone.make_aware(datetime(created_at_min_year, created_at_min_month, created_at_min_day, created_at_min_hour, created_at_min_minute), timezone.get_default_timezone())
                max_date = timezone.make_aware(datetime(created_at_max_year, created_at_max_month, created_at_max_day, created_at_max_hour, created_at_max_minute), timezone.get_default_timezone())
                news = news.filter(created_at__range=(min_date, max_date))
            
            
            return render(request, 'app/home.html', {'form': form, 'news': news, 'filter': filter})
        else:
            return render(request, 'app/home.html', {'form': form, 'filter': filter})
    
    
class SearchTask(ListView):
    model = NewsBase
    template_name = 'app/task_list.html'
    context_object_name = 'news'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        return NewsBase.objects.filter(title__iregex=q).select_related('category')


    
def NewsContent(request, news_id): 
    news = get_object_or_404(NewsBase, pk=news_id)
    
    if news.is_published == True:
        try:
            author_name = news.author.user.username
            author_info = UserBase.objects.get(user__username=author_name)
            user_articles_id = UserBase.objects.values(news = F('GetAuthors')).filter(user__username=author_name)
            cnt_articles = len(user_articles_id)
            authors_news = NewsBase.objects.filter(pk__in=user_articles_id)
        except:
            author_name = 'неизвестен'
            author_info = None
            authors_news = None
            cnt_articles = 0

        try:
            comments = CommentsBase.objects.filter(news_title__pk=news_id).select_related('user__user_base', 'user')
            comments_quentity = len(comments)
        except:
            comments = None
            comments_quentity = 0
            
        news.views = F('views') + 1
        news.save()
        news.refresh_from_db() 
        
        if request.method == 'POST':
            form = LeaveCommentForm(request.POST)
            if form.is_valid():
                user_instance = User.objects.get(username=request.user.username)
                news_instance = NewsBase.objects.get(title=news.title)
                CommentsBase.objects.create(user=user_instance, news_title=news_instance, user_comment=form.cleaned_data['user_comment'])
                messages.success(request, 'Ваш комментарий успешно опубликован!')
                return redirect('news-content', news_id)
            
        else:
            form = LeaveCommentForm()
    
        return render(request, 'app/news.html', {
            'news': news,
            'title': news.title,
            'author_name': author_name,
            'authors_news': authors_news,
            'author_info': author_info,
            'cnt_articles': cnt_articles,
            'form': form,
            'comments': comments,
            'comments_quentity': comments_quentity,
        })
    
    else:
        return HttpResponse('Статья находится на этапе проверки')


class CreateNewsView(CreateView):
    form_class = CreateNewsForm
    template_name = 'app/add_news.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Опубликовать новость'
        return context

    def form_valid(self, form):
        user_base = UserBase.objects.get(user=self.request.user)
        form.instance.author = user_base
        messages.success(self.request, 'Ваша статья отправлена на проверку, после одобрения она появится в списке новостей')
        return super().form_valid(form)