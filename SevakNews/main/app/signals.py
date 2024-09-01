from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags

from .models import NewsBase
from Users.user_models import UserBase
        
        
@receiver(post_save, sender=NewsBase)
def verificate(sender, created, instance, **kwargs):
    if created:
        html_content = (
            f'Пользователь {instance.author} хочет опубликовать новость «{instance.title}»' \
            f'по категории {instance.category}.\n\n' \
            f'{instance.content}'
        )
        
        text_content = (
            f'Пользователь {instance.author} хочет опубликовать новость «{instance.title}»' \
            f'по категории {instance.category}.\n\n' \
            f'{strip_tags(instance.content)}'
        )

        message = EmailMultiAlternatives('Верификация новости', text_content, 'sevak.grigoryan.06@mail.ru', ['send_message.23@mail.ru'])
        message.attach_alternative(html_content, "text/html")
        message.send(fail_silently=True)
        
        
@receiver(post_save, sender=NewsBase)
def send_the_news_to_subscribers(sender, instance, created, **kwargs):
    if instance.is_published == True and instance.views == 0:
        text_content = (
            f'Пользователь {instance.author} опубликовать новость «{instance.title}»' \
            f'по категории {instance.category}.\n\n' \
            f'Зайди быстрее чтобы прочитать и оставить свое мнение!'
        )

        users_emails = [item['email'] for item in list(User.objects.filter(user_base__notification=True).values('email'))]
        
        send_mail(
            'Появилась новая статья',
            text_content,
            'sevak.grigoryan.06@mail.ru',
            users_emails,
            fail_silently=True,
        )