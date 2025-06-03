from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import UserProfile, AccessProfile, Permission, UserAccessProfile
from .utils import update_user_password, create_user_with_profile
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'profile_picture', 'theme_preference', 'email_notifications', 'system_notifications']


class PermissionSerializer(serializers.ModelSerializer):
    module_display = serializers.CharField(source='get_module_display', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'module', 'module_display', 'action', 'action_display']


class AccessProfileSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = AccessProfile
        fields = ['id', 'name', 'description', 'permissions', 'created_at', 'updated_at']


class UserAccessProfileSerializer(serializers.ModelSerializer):
    access_profile = AccessProfileSerializer(read_only=True)
    access_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=AccessProfile.objects.all(),
        source='access_profile',
        write_only=True
    )
    
    class Meta:
        model = UserAccessProfile
        fields = ['id', 'access_profile', 'access_profile_id']


class BaseUserSerializer(serializers.ModelSerializer):
    """Serializer base para usuários com funcionalidades comuns."""
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'role', 'profile']
    
    def validate_role(self, value):
        """Valida se o papel é válido."""
        role_choices = getattr(User, 'ROLE_CHOICES', None)
        if not role_choices or value not in dict(role_choices):
            raise serializers.ValidationError("Papel inválido. Escolha um dos papéis válidos.")
        return value


class UserSerializer(BaseUserSerializer):
    """Serializer para operações de usuário (leitura, atualização)."""
    access_profiles = UserAccessProfileSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['id', 'is_active', 'date_joined', 'password', 'access_profiles']
        read_only_fields = ['date_joined']
    
    def create(self, validated_data):
        """Cria um novo usuário com perfil."""
        return create_user_with_profile(validated_data)
    
    def update(self, instance, validated_data):
        """Atualiza um usuário existente e seu perfil."""
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update password if provided
        if password:
            update_user_password(instance, password)
        else:
            instance.save()
        
        # Update Profile fields
        if profile_data and hasattr(instance, 'profile'):
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        
        return instance


class UserCreateSerializer(BaseUserSerializer):
    """Serializer para criação de usuários com validação de senha."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['password']
    
    def validate(self, attrs):
        # Define o papel padrão se não for especificado
        if 'role' not in attrs:
            attrs['role'] = 'TEAM_MEMBER'
        return attrs
    
    def create(self, validated_data):
        """Cria um novo usuário com perfil."""
        return create_user_with_profile(validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para alteração de senha com validação da senha atual."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        """Valida se a senha atual está correta."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta")
        return value
    
    def save(self):
        """Salva a nova senha e atualiza campos relacionados."""
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        return update_user_password(user, new_password)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, validators=[validate_password])
    token = serializers.CharField(required=True)
    
    def validate_password(self, value):
        # Additional password validation logic could be added here
        return value
