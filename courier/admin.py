from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Signup

class CustomUserAdmin(UserAdmin):
    model = Signup
    list_display = ('email', 'ownername', 'company_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Company Info', {'fields': ('company_name', 'ownername', 'address', 'contact')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'ownername', 'address', 'contact', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Signup, CustomUserAdmin)
