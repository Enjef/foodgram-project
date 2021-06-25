from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView,
    PasswordResetDoneView, PasswordResetView
)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    CreationForm, CustomAuthenticationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm
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
    template_name = 'users/resetPassword.html'
    domain = 'sprint.ml'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/resetPassword_done.html'


class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/changePassword.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/changePassword_done.html'
