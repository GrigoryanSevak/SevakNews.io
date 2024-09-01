import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User

from .models import Room, Message
from Users.user_models import UserBase


@receiver(post_save, sender=UserBase)
def create_room(sender, created, instance, **kwargs):
    if created:
        room_name = instance.user.username
        uid = str(''.join(random.choices(string.ascii_letters + string.digits, k=4)))
        room_slug = slugify(room_name + "_" + uid)
        Room.objects.create(name=room_name, slug=room_slug, main_user=instance.user)
        
        room = Room.objects.get(slug=room_slug)
        room.users.add(instance.user)
        # Ensure you're adding the User instance, not UserBase
        admin_user = User.objects.get(username="Admin")
        room.users.add(admin_user)
        room.save()
        
        