"""Add users to Django Admin."""

from django import forms
from django.contrib import admin
from .models import User
from rest_framework.authtoken.models import TokenProxy


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_superuser', 'user_permissions']
        readonly_fields = ['last_login', 'date_joined']


class UserAdmin(admin.ModelAdmin):
    exclude = ['password', 'is_staff', 'is_superuser', 'user_permissions']
    readonly_fields = ['last_login', 'date_joined']
    form = UserForm


admin.site.register(User, UserAdmin)
admin.site.unregister(TokenProxy)
