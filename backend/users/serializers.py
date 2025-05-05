from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import UserProfile, AccessProfile, Permission, UserAccessProfile

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    access_profiles = UserAccessProfileSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'role', 'is_active', 
                  'date_joined', 'profile', 'password', 'access_profiles']
        read_only_fields = ['date_joined']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update User fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        
        instance.save()
        
        # Update Profile fields
        if profile_data and hasattr(instance, 'profile'):
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'role', 'password']
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            role=validated_data['role']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        # Create default profile
        UserProfile.objects.create(user=user)
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.password_change_required = False
        user.last_password_change = timezone.now()
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, validators=[validate_password])
    token = serializers.CharField(required=True)
    
    def validate_password(self, value):
        # Additional password validation logic could be added here
        return value
