from django.contrib import admin
from .models import Room, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    save_on_top = True
    

class MessageAdmin(admin.ModelAdmin):
    save_on_top = True
    
    
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)


admin.site.site_header = 'Управление новостями'
admin.site.site_title = 'Управление сообщениями'