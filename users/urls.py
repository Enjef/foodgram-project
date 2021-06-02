from django.urls import path, include
from users.views import (
    Logout, SignUp, Login, PasswordReset, PasswordChange
)

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('', include('django.contrib.auth.urls')),
]
