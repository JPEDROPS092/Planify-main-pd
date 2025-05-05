from django.contrib import admin
from .models import User, UserProfile, AccessProfile, Permission, UserAccessProfile, PasswordHistory

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = get_all_fields(User)
    list_filter = get_all_fields(User)
    search_fields = ['username', 'email', 'full_name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = get_all_fields(UserProfile)
    list_filter = get_all_fields(UserProfile)
    search_fields = ['user__username', 'phone']

@admin.register(AccessProfile)
class AccessProfileAdmin(admin.ModelAdmin):
    list_display = get_all_fields(AccessProfile)
    list_filter = get_all_fields(AccessProfile)
    search_fields = ['name']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Permission)
    list_filter = get_all_fields(Permission)
    search_fields = ['module', 'action']

@admin.register(UserAccessProfile)
class UserAccessProfileAdmin(admin.ModelAdmin):
    list_display = get_all_fields(UserAccessProfile)
    list_filter = get_all_fields(UserAccessProfile)
    search_fields = ['user__username', 'access_profile__name']

@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
    list_display = get_all_fields(PasswordHistory)
    list_filter = get_all_fields(PasswordHistory)
    search_fields = ['user__username']
