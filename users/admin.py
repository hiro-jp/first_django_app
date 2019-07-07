from users.models import Unit
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _


@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('employee_code', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_approver', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Skills'), {'fields': ('skill_group_follow', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
