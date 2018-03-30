from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count

from .models import User


# Hide built-in group administration
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'vendor', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_display = ('username', 'email', 'is_staff', 'deal_count', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'vendor')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('username', 'email')

    def get_queryset(self, request):
        # Include count of submitted deals
        qs = super().get_queryset(request)
        return qs.annotate(deal_count=Count('deals'))

    def deal_count(self, instance):
        return instance.deal_count
    deal_count.admin_order_field = 'deal_count'
    deal_count.short_description = 'Deals'
