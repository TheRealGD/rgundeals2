from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .forms import RegistrationForm
from .models import User


class UserView(View):
    """
    Display the profile/comments for a particular user
    """
    template_name = 'users/user.html'

    def get(self, request, username):

        user = get_object_or_404(User, username=username)

        return render(request, self.template_name, {
            'user': user,
        })


class UserRegistrationView(View):
    """
    Register a new user account
    """
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        form = RegistrationForm()

        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):

        form = RegistrationForm(data=request.POST)

        if form.is_valid():

            # Create the new User
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Log the user in
            login(request, user)

            messages.success(request, "You have successfully registered!")

            return redirect('home')


class LoginView(View):
    """
    Authenticate a user using the provided username and password
    """
    template_name = 'users/login.html'

    def get(self, request):

        form = AuthenticationForm(request)

        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            # Log the user in
            user = form.get_user()
            login(request, user)

            return redirect('home')

        return render(request, self.template_name, {
            'form': form,
        })


class LogoutView(View):
    """
    De-authenticate a user
    """

    def get(self, request):

        # Log the user out
        logout(request)

        messages.info(request, "You have been logged out.")

        return redirect('home')
