from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView, LogoutView ,PasswordResetView, PasswordChangeView
)

from django.urls import reverse_lazy

from .forms import (
    CreationForm, CustomAuthenticationForm, CustomPasswordResetForm,
    CustomPasswordChangeForm,
)


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'users/reg.html'


class Login(LoginView):
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'users/authForm.html'


class Logout(LogoutView):
    template_name = 'users/logout.html'


class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('index')
    template_name = 'users/resetPassword.html'


class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'users/changePassword.html'
