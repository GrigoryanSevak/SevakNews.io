from django.contrib import admin
from .user_models import UserBase
from ckeditor_uploader.widgets import CKEditorUploadingWidget
    
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'notification')
    list_display_links = ('id', 'user')
    list_editable = ('notification',)
    search_fields = ('user', 'first_name', 'last_name')
    list_filter = ('register_in', 'notification')
    readonly_fields = ('register_in',)
    save_on_top = True
    
    
admin.site.register(UserBase, UserAdmin)

admin.site.site_header = 'Управление новостями'
admin.site.site_title = 'Управление новостями'