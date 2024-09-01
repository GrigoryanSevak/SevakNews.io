from django import forms
from .models import NewsBase, CommentsBase
from captcha.fields import CaptchaField, CaptchaTextInput
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class LeaveCommentForm(forms.ModelForm):
    class Meta:
        model = CommentsBase
        fields = ['user_comment']
        widgets = {
            'user_comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = NewsBase
        fields = ['title', 'content', 'photo', 'category']
        widgets  = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class DateFilterForm(forms.Form):
    filter_date = forms.ChoiceField(
        label='Выберите дату',
        choices=[
            ('today', _('Сегодня')),
            ('yesterday', _('За 2 дня')),
            ('day_before_yesterday', _('За 3 дня')),
            ('all_days', _('За все время')),
        ],
        initial='all_days',
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'date_check'})
    )
    views = forms.IntegerField(
        label=_('Количество просмотров'),
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10000, 'value': 10000, 'step': 100, 'oninput': "this.nextElementSibling.value = this.value"}),
    )