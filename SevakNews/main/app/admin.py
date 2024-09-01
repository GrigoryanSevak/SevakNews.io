from django.contrib import admin
from .models import NewsBase, NewsCategory, CommentsBase
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = NewsBase
        fields = '__all__'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'news_title', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('created_at',)
    search_fields = ('user', 'news_title')
    readonly_fields = ('created_at',)
    save_on_top = True
    

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'is_published', 'created_at', 'views', 'category')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created_at', 'updated_at', 'views', 'category')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'views')
    save_on_top = True
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    save_on_top = True
    
    
admin.site.register(NewsBase, NewsAdmin)
admin.site.register(NewsCategory, CategoryAdmin)
admin.site.register(CommentsBase, CommentsAdmin)

admin.site.site_header = 'Управление новостями'
admin.site.site_title = 'Управление новостями'