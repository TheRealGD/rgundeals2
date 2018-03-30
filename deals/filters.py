import django_filters

from .models import Category, Deal, Vendor


class DealFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        method='filter_category'
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

    def filter_category(self, queryset, name, value):
        try:
            category = Category.objects.get(slug=value)
        except Category.DoesNotExist:
            return queryset.none()
        return queryset.filter(
            category__in=category.get_descendants(include_self=True)
        )

    def filter_domain(self, queryset, name, value):
        return queryset.filter(url__icontains=value)
