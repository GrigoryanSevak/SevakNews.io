from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class CommentsBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='GetComments')
    news_title = models.ForeignKey('NewsBase', on_delete=models.CASCADE, verbose_name='Статья')
    user_comment = models.TextField(max_length=5000, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    def get_absolute_url(self):
        return reverse("UserPage", kwargs={"username": self.user})
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.news_title.title}"
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at', 'news_title']
        

class NewsBase(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=254)
    content = RichTextUploadingField(verbose_name='Содержимое')
    photo = models.ImageField(upload_to='News-photos/%Y/%m/%d/', verbose_name='Фотография', blank=False, default='default.jpg')
    is_published = models.BooleanField(verbose_name='Опубликовано', default=False)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обнавлено', auto_now=True)
    views = models.IntegerField(verbose_name='Количество просмотров', default=0)
    category = models.ForeignKey('NewsCategory', verbose_name='Категория', on_delete=models.PROTECT, null=True, blank=True, related_name='GetNews')
    author = models.ForeignKey('Users.UserBase', verbose_name='Автор', on_delete=models.PROTECT, null=True, blank=True, related_name='GetAuthors', to_field='user')

    def get_absolute_url(self):
        return reverse(viewname="news-content", kwargs={"news_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class NewsCategory(models.Model):
    title = models.CharField(verbose_name='Категория', db_index=True, max_length=254)
    
    def get_absolute_url(self):
        return reverse(viewname="category", kwargs={"title": self.title})
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
        