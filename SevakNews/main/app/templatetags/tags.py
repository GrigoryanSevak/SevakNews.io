from django import template
from app.models import NewsCategory
from django.db.models import Count, F
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag()
def get_categories():
    categories = NewsCategory.objects.annotate(cnt=Count('GetNews', filter=F('GetNews__is_published'))).filter(cnt__gt=0).select_related()
    return categories

@register.filter(name='translate')
def translate(text):
    try:
        return _(text)
    except:
        return text