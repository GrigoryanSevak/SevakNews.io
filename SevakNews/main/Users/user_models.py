import os
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings


class UserBase(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='user_base')
    first_name = models.CharField(verbose_name='Имя', max_length=254, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=254, blank=True)
    photo = models.ImageField(verbose_name='Фото пользователя', upload_to='Users-photo/', blank=True, default=os.path.join(settings.BASE_DIR, 'media/default_login.jpg'))
    register_in = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    notification = models.BooleanField(verbose_name='Уведомления', default=False)
    email_verify = models.BooleanField(verbose_name='Подтверждение почты', default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Пользовательские данные'
        ordering = ['user']
        
        