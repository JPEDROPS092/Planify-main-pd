# Users Module Documentation

## Overview

The Users module is a core component of the Planify system, responsible for user authentication, authorization, and access control. It implements a robust security model with role-based access control (RBAC), permission management, and account security features.

## Key Components

### Models (`models.py`)

- **User**: Custom user model extending Django's `AbstractBaseUser` and `PermissionsMixin`
  - Supports roles (ADMIN, PROJECT_MANAGER, TEAM_MEMBER)
  - Tracks login attempts and account lockout
  - Implements password history and change requirements

- **UserProfile**: Extended user information including contact details and preferences

- **AccessProfile**: Defines sets of permissions that can be assigned to users

- **Permission**: Individual permissions for specific modules and actions

- **UserAccessProfile**: Many-to-many relationship between users and access profiles

- **PasswordHistory**: Tracks password changes to prevent reuse

- **AccessAttempt**: Logs authentication and authorization attempts

### Authentication (`authentication.py`)

- **CustomJWTAuthentication**: Extended JWT authentication that:
  - Supports both header and cookie-based token authentication
  - Implements proper CSRF protection for cookie-based authentication
  - Includes detailed logging of authentication attempts

### Middleware (`middleware.py`)

- **PermissionMiddleware**: Enforces access control by:
  - Mapping URLs to required permissions
  - Checking user permissions against required permissions
  - Logging access attempts
  - Handling account lockout

### Authentication Views (`auth_views.py`)

- **CustomTokenObtainPairView**: JWT token generation with:
  - Account lockout handling
  - Failed login attempt tracking
  - Enhanced token payload with user information

### Registration (`register_views.py`)

- **RegisterView**: Public user registration with default role assignment

### Serializers (`serializers.py`)

- User data serialization and validation
- Password change and reset functionality
- Profile management

## Security Analysis

### Strengths

1. **Role-Based Access Control**: Comprehensive permission system with granular control over module access
2. **Account Lockout**: Protection against brute force attacks by locking accounts after multiple failed attempts
3. **Password History**: Prevents password reuse, enhancing security
4. **JWT with Cookie Support**: Flexible authentication options with proper CSRF protection
5. **Detailed Logging**: Comprehensive logging of authentication and authorization attempts
6. **Transaction Management**: Proper use of database transactions for data integrity

### Areas for Improvement

1. **Password Policies**:
   - No explicit password complexity requirements beyond Django's defaults
   - Consider implementing minimum length, character variety, and common password checks

2. **Multi-Factor Authentication (MFA)**:
   - Currently lacks MFA support
   - Adding TOTP or SMS-based verification would enhance security

3. **Session Management**:
   - No explicit session timeout configuration
   - Consider implementing idle session timeout

4. **Rate Limiting**:
   - No explicit rate limiting for authentication attempts
   - Consider implementing IP-based rate limiting for login endpoints

5. **Audit Trail**:
   - While access attempts are logged, a more comprehensive audit trail for sensitive operations would be beneficial
   - Consider tracking all security-relevant actions (password changes, permission changes, etc.)

6. **Error Messages**:
   - Some error messages could potentially leak information about valid usernames
   - Standardize on generic authentication failure messages

7. **Token Revocation**:
   - No explicit mechanism for revoking active tokens when a user changes password or is deactivated
   - Consider implementing a token blacklist

## Documentation Suggestions

1. **Code Documentation**:
   - Add comprehensive docstrings to all views, serializers, and models
   - Document security-relevant methods and attributes

2. **API Documentation**:
   - Enhance drf_spectacular schema with detailed descriptions
   - Document error responses and status codes

3. **Security Guidelines**:
   - Create documentation for administrators on user management best practices
   - Document password policies and account lockout procedures

## Redundancy Analysis

1. **Serializers**:
   - `UserCreateSerializer` and `UserSerializer` have significant overlap
   - Consider refactoring to reduce duplication

2. **Password Change Logic**:
   - `ChangePasswordSerializer` contains duplicate code for password changes
   - Consider extracting to a utility function

3. **Permission Checking**:
   - Permission checks are implemented in both middleware and views
   - Consider centralizing permission logic

## Implementation Recommendations

1. **Add Multi-Factor Authentication**:
   ```python
   # Example implementation using django-otp
   from django_otp.plugins.otp_totp.models import TOTPDevice
   
   def verify_otp(user, token):
       device = TOTPDevice.objects.get(user=user, confirmed=True)
       return device.verify_token(token)
   ```

2. **Enhance Password Policies**:
   ```python
   # Example custom password validator
   from django.core.exceptions import ValidationError
   
   class ComplexityValidator:
       def validate(self, password, user=None):
           if not any(char.isdigit() for char in password):
               raise ValidationError('Password must contain at least one digit.')
           if not any(char.isupper() for char in password):
               raise ValidationError('Password must contain at least one uppercase letter.')
   ```

3. **Implement Token Revocation**:
   ```python
   # Example token blacklist implementation
   from rest_framework_simplejwt.tokens import TokenError
   from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
   
   def blacklist_user_tokens(user):
       tokens = OutstandingToken.objects.filter(user_id=user.id)
       for token in tokens:
           BlacklistedToken.objects.get_or_create(token=token)
   ```

4. **Add Rate Limiting**:
   ```python
   # Example using Django Rest Framework's throttling
   from rest_framework.throttling import AnonRateThrottle
   
   class LoginRateThrottle(AnonRateThrottle):
       rate = '5/min'
   ```

## Conclusion

The Users module provides a solid foundation for authentication and authorization in the Planify system. By implementing the suggested improvements, the security posture can be further enhanced to meet industry best practices for user management and access control.
