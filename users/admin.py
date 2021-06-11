from users.forms import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class PersonAdmin(UserAdmin):
    list_filter = ('email', 'username',)


admin.site.unregister(User)
admin.site.register(User, PersonAdmin)
