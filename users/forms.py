from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserCreationForm)
from django.core.exceptions import ValidationError


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2',)

    def clean(self):
        email = self.cleaned_data.get('email')
        dubble = User.objects.filter(email=email)
        if dubble:
            raise ValidationError('Email exists')
        return self.cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2',)
