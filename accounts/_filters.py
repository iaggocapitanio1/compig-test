import django_filters
from .models import *


class LoadingFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='publication', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='publication', lookup_expr='lte')
    producer = django_filters.CharFilter(field_name='truck__producer__name', lookup_expr='icontains')

    class Meta:
        model = Loading
        fields = {
            'quantity':  ['lt', 'gt']

        }