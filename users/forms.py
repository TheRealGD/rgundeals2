from django import forms
from django.core.validators import MinLengthValidator

from .models import User
from .validators import UsernameValidator


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        validators=[UsernameValidator()]
    )
    email = forms.EmailField(
        max_length=254
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[MinLengthValidator(12)],
        label='Password',
        help_text="Choose a strong password (12 characters minimum)"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password (again)',
        help_text="Password again for verification"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
