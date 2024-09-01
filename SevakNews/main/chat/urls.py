from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    # path("404_error/", TemplateView.as_view(template_name='technical_404.html'), name='404_error'),
    path("techical_supprot/<str:slug>/", views.TechnicalSupport.as_view(), name='chat'),
    # path("room/<str:slug>/", views.index, name='chat'),
#     path("create/", views.room_create, name='room-create'),
#     path("join/", views.room_join, name='room-join'),
]
