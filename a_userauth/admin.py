from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('registration_number', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('registration_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','is_verified',)}),
        ('Permissions', {'fields': ('role','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('registration_number', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('registration_number', 'first_name', 'last_name', 'email')
    ordering = ('created_at',)


# Register your User model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmailOTP)
admin.site.register(RegistrationCode)