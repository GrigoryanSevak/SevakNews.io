import string
import random

from django.urls import reverse
from django.db.models import Q
from django.http import Http404
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import ListView
from django.contrib.auth.models import User
from Users.user_models import UserBase

from chat.models import Room, Message

from django.views.generic import ListView
from django.shortcuts import redirect

class TechnicalSupport(ListView):
    model = Room
    template_name = 'chat/room.html'
    context_object_name = 'message'

    def dispatch(self, request, *args, **kwargs):
        slug_parts = self.kwargs['slug'].split('_')[0]
        if not (request.user.is_superuser or 
                Room.objects.filter(name__iregex=slug_parts, users__username=request.user.username).exists()):
            return render(request, 'technical_404.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Техническая поддержка'
        context['slug'] = room.slug
        context['user'] = room.main_user.user_base
        return context

    def get_queryset(self):
        room = Room.objects.get(slug=self.kwargs['slug'])
        return Message.objects.filter(room__name=room.name).select_related('user__user_base')