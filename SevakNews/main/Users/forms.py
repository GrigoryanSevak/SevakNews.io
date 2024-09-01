from django import forms
from .user_models import UserBase
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
import re


class SendMassMailForm(forms.Form):
    title = forms.CharField(label='Тема', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    content = forms.CharField(widget=CKEditorWidget, label='Содержимое')


class SetUserNotificationForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        "type": "email",
        "placeholder": "Enter your email address"
    }))


class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ['first_name', 'last_name', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Никнейм', max_length=150, widget=forms.TextInput(attrs={
                                   'type': "text",
                                   'id': 'name'
                                }))
    first_name = forms.CharField(label='Имя', max_length=254, required=False, widget=forms.TextInput(attrs={
                                    'type': "text",
                                    'id': 'first_name'
                                }))
    last_name = forms.CharField(label='Фамилия', max_length=254, required=False, widget=forms.TextInput(attrs={
                                    'type': "text",
                                    'id': 'last_name'
                                }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                   'type': "email",
                                   'id': "email",
                                }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
                                   'type': "password",
                                   'id': "password",
                                }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
                                   'type': "password",
                                   'id': "confirm-password",
                                }))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_base = UserBase(user=user, first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'])
            user_base.save()
        return user
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150, 
                               widget=forms.TextInput(attrs={
                                   'type': "text",
                                   'id': 'name'
                                }))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                    'type': "password",
                                    'id': "password",
                                }))