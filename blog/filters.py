import django_filters
from django.db.models import Q


class NewsFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method='search_filter')



    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(text__icontains=value)
        )