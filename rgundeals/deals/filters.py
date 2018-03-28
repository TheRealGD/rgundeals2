import django_filters

from .models import Category, Deal, Vendor


class DealFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        name='category__slug',
        to_field_name='slug'
    )
    vendor = django_filters.ModelMultipleChoiceFilter(
        queryset=Vendor.objects.all(),
        name='vendor__slug',
        to_field_name='slug'
    )
    domain = django_filters.CharFilter(
        method='filter_domain'
    )

    class Meta:
        model = Deal
        fields = ['created_by', 'category', 'vendor']

    def filter_domain(self, queryset, name, value):
        return queryset.filter(url__icontains=value)
