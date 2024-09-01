from django.db import models
from django.urls import reverse

from Users.user_models import UserBase
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(verbose_name='Название чата', max_length=128)
    slug = models.SlugField(verbose_name='Идентификатор чата', unique=True)
    main_user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=None, related_name='main_room')
    users = models.ManyToManyField(User, verbose_name='Участники', related_name='rooms')
    
    def get_absolute_url(self):
        return reverse(viewname="chat", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, verbose_name='Чата', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(verbose_name='Дата отправки', auto_now_add=True)

    def __str__(self):
        return (
            self.room.name + " - " +
            str(self.user.username) + " : " +
            str(self.message)
        )
        
        