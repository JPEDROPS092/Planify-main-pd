from django.contrib import admin
from .models import User, UserProfile, AccessProfile, Permission, UserAccessProfile, PasswordHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'full_name', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined', 'role']
    search_fields = ['username', 'email', 'full_name']
    date_hierarchy = 'date_joined'
    readonly_fields = ['date_joined', 'last_login']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'theme_preference']
    list_filter = ['theme_preference']
    search_fields = ['user__username', 'user__email', 'phone']
    autocomplete_fields = ['user']

# Registros simples sem customização
admin.site.register(AccessProfile)
admin.site.register(Permission)
admin.site.register(UserAccessProfile)
admin.site.register(PasswordHistory)