from django.contrib import admin

from .models import Client, TenantInvitation, TenantMembership, TenantSettings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'on_trial', 'paid_until', 'created_on']
    list_filter = ['on_trial', 'created_on']
    search_fields = ['name']


@admin.register(TenantMembership)
class TenantMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'tenant']
    search_fields = ['user__username', 'user__email', 'tenant__name']
    autocomplete_fields = ['user', 'tenant']


@admin.register(TenantInvitation)
class TenantInvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'tenant', 'role', 'status', 'invited_by', 'created_at', 'expires_at']
    list_filter = ['status', 'role', 'tenant']
    search_fields = ['email', 'tenant__name']
    autocomplete_fields = ['tenant', 'invited_by', 'accepted_user']
    readonly_fields = ['token', 'status', 'accepted_user', 'accepted_at', 'created_at', 'updated_at']


@admin.register(TenantSettings)
class TenantSettingsAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'updated_at']
    search_fields = ['tenant__name']
    autocomplete_fields = ['tenant']
    readonly_fields = ['created_at', 'updated_at']
