from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import User, UserProfile, AccessProfile, Permission, UserAccessProfile, PasswordHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'full_name', 'role', 'is_active', 'is_staff', 'last_login']
    list_filter = ['is_active', 'is_staff', 'role', 'date_joined', 'last_login']
    search_fields = ['username', 'email', 'full_name']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']
    actions = ['make_active', 'make_inactive']
    
    fieldsets = [
        (_('Informações de Login'), {'fields': ['username', 'email', 'password']}),
        (_('Informações Pessoais'), {'fields': ['full_name', 'role']}),
        (_('Permissões'), {
            'fields': ['is_active', 'is_staff', 'is_superuser'],
            'classes': ['collapse']
        }),
        (_('Datas Importantes'), {'fields': ['last_login', 'date_joined']}),
    ]
    
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['username', 'email', 'full_name', 'password1', 'password2', 'role'],
        }),
    ]
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} usuários foram ativados com sucesso.')
    make_active.short_description = "Ativar usuários selecionados"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} usuários foram desativados com sucesso.')
    make_inactive.short_description = "Desativar usuários selecionados"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'phone', 'get_profile_picture']
    search_fields = ['user__username', 'user__email', 'phone']
    autocomplete_fields = ['user']
    
    fieldsets = [
        (_('Usuário'), {'fields': ['user']}),
        (_('Informações de Contato'), {'fields': ['phone', 'address']}),
        (_('Informações Profissionais'), {'fields': ['department', 'position', 'bio']}),
        (_('Imagem de Perfil'), {'fields': ['profile_picture']}),
    ]
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Usuário'
    get_username.admin_order_field = 'user__username'
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>', obj.profile_picture.url)
        return "Sem imagem"
    get_profile_picture.short_description = 'Foto'


@admin.register(AccessProfile)
class AccessProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_permissions_count']
    search_fields = ['name', 'description']
    
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
    ]
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = 'Permissões'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['module', 'action', 'access_profile']
    list_filter = ['module', 'action']
    search_fields = ['module', 'action', 'access_profile__name']
    fieldsets = [
        (None, {'fields': ['access_profile', 'module', 'action']}),
    ]


@admin.register(UserAccessProfile)
class UserAccessProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'access_profile']
    list_filter = ['access_profile']
    search_fields = ['user__username', 'user__email', 'access_profile__name']
    autocomplete_fields = ['user', 'access_profile']
    fieldsets = [
        (None, {'fields': ['user', 'access_profile']}),
    ]


@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    autocomplete_fields = ['user']
    date_hierarchy = 'created_at'
    readonly_fields = ['password_hash', 'created_at']
    
    fieldsets = [
        (None, {'fields': ['user', 'password_hash', 'created_at']}),
    ]
    
    def has_add_permission(self, request):
        return False
