
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import (
    AddUserForm, ChangeUserForm, ChangeAdminPasswordForm
)


# Register your models here.
class QUserAdmin(UserAdmin):
    form = ChangeUserForm
    add_form = AddUserForm
    change_password_form = ChangeAdminPasswordForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            ('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            ('Permissions'), {'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login',)}),
    )

    restricted_fieldsets = (
        (None, {'fields': ('email',)}),
        (
            ('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            ('Permissions'), {'fields': ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email',
                       'password1', 'password2'),
        }),
    )

    non_admin_read_only_fields = ('email', 'password')

    ordering = ('email',)
    list_display = ('__str__', 'first_name', 'last_name',
                    'is_active', 'is_superuser', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, QUserAdmin)
