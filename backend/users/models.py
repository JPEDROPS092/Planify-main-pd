from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not full_name:
            raise ValueError('Users must have a full name')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('PROJECT_MANAGER', 'Project Manager'),
        ('TEAM_MEMBER', 'Team Member'),
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TEAM_MEMBER')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    password_change_required = models.BooleanField(default=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.password_change_required and self.last_password_change is None:
            self.last_password_change = timezone.now()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    THEME_CHOICES = (
        ('LIGHT', 'Light'),
        ('DARK', 'Dark'),
        ('SYSTEM', 'System'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    theme_preference = models.CharField(max_length=10, choices=THEME_CHOICES, default='SYSTEM')
    email_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class AccessProfile(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    MODULE_CHOICES = (
        ('PROJECTS', 'Projects'),
        ('TASKS', 'Tasks'),
        ('TEAMS', 'Teams'),
        ('RESOURCES', 'Resources'),
        ('COMMUNICATIONS', 'Communications'),
        ('RISKS', 'Risks'),
        ('COSTS', 'Costs'),
        ('DOCUMENTS', 'Documents'),
        ('REPORTS', 'Reports'),
    )
    
    ACTION_CHOICES = (
        ('VIEW', 'View'),
        ('CREATE', 'Create'),
        ('EDIT', 'Edit'),
        ('DELETE', 'Delete'),
    )
    
    access_profile = models.ForeignKey(AccessProfile, on_delete=models.CASCADE, related_name='permissions')
    module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    
    class Meta:
        unique_together = ('access_profile', 'module', 'action')
    
    def __str__(self):
        return f"{self.access_profile.name} - {self.get_module_display()} - {self.get_action_display()}"


class UserAccessProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_profiles')
    access_profile = models.ForeignKey(AccessProfile, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'access_profile')
    
    def __str__(self):
        return f"{self.user.username} - {self.access_profile.name}"


class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
