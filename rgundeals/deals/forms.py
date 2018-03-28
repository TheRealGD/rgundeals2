from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import Category, Deal


class DealForm(forms.ModelForm):
    """
    Create or edit a Deal
    """
    category = TreeNodeChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Deal
        fields = (
            'title', 'url', 'category', 'price', 'qty', 'discount', 'expires',
            'coupon_code', 'description',
        )
        help_texts = {
            'price': 'Base price in USD (do not include tax/shipping)',
            'qty': 'Number of items/rounds; used to calculate unit cost (optional)',
            'expires': 'Date/time at which this deal expires (optional)<br />'
                       'Format: YYYY-MM-DD [hh:mm:ss]'
        }


class ModDealForm(DealForm):
    """
    Extends DealForm with additional fields for moderators
    """

    class Meta(DealForm.Meta):
        fields = (
            'title', 'url', 'category', 'price', 'qty', 'discount', 'expires',
            'coupon_code', 'description', 'vendor', 'locked',
        )


class ConfirmationForm(forms.Form):
    """
    Generic form used to confirm a potentially dangerous action (e.g. deleting
    an object)
    """
    confirmed = forms.BooleanField(widget=forms.HiddenInput)
