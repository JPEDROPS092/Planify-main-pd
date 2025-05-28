from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Voce Precisa de um endereço de e-mail')
        if not username:
            raise ValueError('Users deve ter username')
        if not full_name:
            raise ValueError('Users deve ter  full name')
        
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
        ('TEAM_LEADER', 'Team Leader'),
        ('TEAM_MEMBER', 'Team Member'),
        ('STAKEHOLDER', 'Stakeholder/Client'),
        ('AUDITOR', 'Auditor'),
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
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.password_change_required and self.last_password_change is None:
            self.last_password_change = timezone.now()
        super().save(*args, **kwargs)
    
    def increment_failed_login(self):
        """Incrementa o contador de tentativas falhas de login e bloqueia a conta se necessário"""
        self.failed_login_attempts += 1
        self.last_login_attempt = timezone.now()
        
        # Bloquear a conta após 5 tentativas falhas
        if self.failed_login_attempts >= 5:
            self.is_locked = True
            
        self.save(update_fields=['failed_login_attempts', 'is_locked'])
    
    def reset_failed_login(self):
        """Reseta o contador de tentativas falhas de login após um login bem-sucedido"""
        self.failed_login_attempts = 0
        self.is_locked = False
        self.save(update_fields=['failed_login_attempts', 'is_locked'])
    
    def has_permission(self, module, action):
        """Verifica se o usuário tem permissão para realizar uma ação em um módulo"""
        # Administradores têm acesso total
        if self.role == 'ADMIN' or self.is_superuser:
            return True
            
        # Verificar permissões específicas através dos perfis de acesso
        for user_profile in self.access_profiles.all():
            if user_profile.access_profile.permissions.filter(module=module, action=action).exists():
                return True
                
        return False


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
        ('USERS', 'Users'),
        ('SETTINGS', 'Settings'),
        ('DASHBOARD', 'Dashboard'),
        ('NOTIFICATIONS', 'Notifications'),
        ('APPROVALS', 'Approvals'),
    )
    
    ACTION_CHOICES = (
        ('VIEW', 'View'),
        ('CREATE', 'Create'),
        ('EDIT', 'Edit'),
        ('DELETE', 'Delete'),
        ('APPROVE', 'Approve'),
        ('ASSIGN', 'Assign'),
        ('EXPORT', 'Export'),
        ('IMPORT', 'Import'),
        ('COMMENT', 'Comment'),
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


class AccessAttempt(models.Model):
    """Modelo para registrar tentativas de acesso a recursos protegidos"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_attempts')
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    success = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Access Attempt'
        verbose_name_plural = 'Access Attempts'
    
    def __str__(self):
        status = 'Success' if self.success else 'Failed'
        return f"{self.user.username} - {self.endpoint} - {status} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
