import django_filters
from django_filters.widgets import DateRangeWidget
from .models import NewsBase
import datetime

class DateFilter(django_filters.FilterSet):
    now = datetime.datetime.now()
    created_at = django_filters.DateTimeFromToRangeFilter(
        widget=DateRangeWidget(
            attrs={
                'id': 'datetime',
                'class': 'form-control',
                'placeholder': f'{now.strftime("%Y-%m-%d")} 00:00',
            }
        )
    )

    class Meta:
        model = NewsBase
        fields = ['created_at']