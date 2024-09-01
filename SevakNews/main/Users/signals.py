from Users.user_models import UserBase

def create_or_update_user_base(sender, instance, created, **kwargs):
    if created:
        # Check if UserBase instance already exists for the user
        if UserBase.objects.filter(user=instance).exists():
            # Handle the case where it already exists, e.g., update it
            user_base = UserBase.objects.get(user=instance)
            user_base.first_name = instance.first_name
            user_base.last_name = instance.last_name
            user_base.save()
        else:
            UserBase.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
    else:
        user_base, _ = UserBase.objects.get_or_create(user=instance)
        user_base.first_name = instance.first_name
        user_base.last_name = instance.last_name
        user_base.save()