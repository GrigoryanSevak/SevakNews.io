from django.urls import path
from django.views.generic import TemplateView
from .views import EmailVerify, register, user_login, user_logout, SendMassMailView, not_authenticated
from . import views

urlpatterns = [
    path('sign_up/', register, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('send_mass_mail/', SendMassMailView, name='send_mass_mail'),
    path('not_authenticated/', not_authenticated, name='not_authenticated'),
    path('user/<str:username>/', views.UserPage.as_view(), name='UserPage'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='Users/invalid_verify.html'), name='invalid_verify'),
    path('confirm_email/', TemplateView.as_view(template_name='Users/confirm_email.html'), name='confirm_email'),
]