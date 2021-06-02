from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
)
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ('email')


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
