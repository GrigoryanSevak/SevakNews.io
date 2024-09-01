from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import SetUserNotificationForm
from Users.user_models import UserBase
from app.models import NewsBase
from django.core.mail import send_mail
from chat.models import Room


def SetUserNotificationView(request):
    if 'subscribe' in request.POST:
        if request.user.is_authenticated:
            if request.method == 'POST':
                form3 = SetUserNotificationForm(request.POST)
                if form3.is_valid():
                    get_email = form3.cleaned_data['email']
                    user = User.objects.get(username=request.user.username)
                    userbase = UserBase.objects.get(user__username=request.user.username)
                    
                    if get_email == user.email:
                        if userbase.notification == False:
                            userbase.notification = True
                            userbase.save()
                            messages.success(request, 'Теперь вы будете получать самые свежие новости!')
                            send_mail(f'Администрация SevakNews',
                                        f'Уважаемый {userbase.first_name} {userbase.last_name}\n\n'\
                                        f'Мы рады сообщить вам, что ваша подписка на SevakNews успешно оформлена. '\
                                        f'Теперь вы будете одним из первых получать информацию о новых статьях, '\
                                        f'доступных на нашей платформе!',
                                        'sevak.grigoryan.06@mail.ru',
                                        [user.email], fail_silently=True)
                        else:
                            messages.info(request, 'Вы уже подписаны!')
                    else:
                        messages.error(request, 'Ошибка, проверьте введенную почту')
                else:
                    messages.error(request, 'Ошибка, проверьте введенную почту')
            else:     
                form3 = SetUserNotificationForm()
        
        else:
            if request.method == 'POST':
                messages.error(request, 'Чтобы подписаться и получать свежие новости, нужно авторизоваться!')
            form3 = SetUserNotificationForm()
    
    else:
        form3 = SetUserNotificationForm()

    news = NewsBase.objects.filter(is_published=True).select_related('category')
    paginator = Paginator(list(news), 6)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    
    if request.user.is_authenticated:
        try:
            chat = Room.objects.get(main_user=request.user) 
            return {'form3': form3, 'news': news[:6], 'page_obj': page_objects, 'chat': chat}
        except:
            pass
    
    return {'form3': form3, 'news': news[:6], 'page_obj': page_objects}
        