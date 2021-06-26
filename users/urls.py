from django.urls import path, include
from users.views import (
    Logout, SignUp, Login, PasswordReset, PasswordChange, PasswordResetDone,
    PasswordChangeDone, PasswordResetComplete, PasswordResetConfirm
)

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path(
        'password_reset/done/',
        PasswordResetDone.as_view(),
        name='password_reset_done'
    ),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path(
        'password_change/done/',
        PasswordChangeDone.as_view(),
        name='password_change_done'
    ),
    path(
        'reset/done/',
        PasswordResetComplete.as_view(),
        name='password_reset_complete'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirm.as_view(),
        name='password_reset_confirm'
    ),
    path('', include('django.contrib.auth.urls')),
]
