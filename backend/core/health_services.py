"""
Business logic services for system health monitoring.
"""
import os
import psutil
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class HealthService:
    """Service class for system health checks and monitoring."""
    
    @staticmethod
    def get_database_status():
        """Check database connectivity and performance."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return {
                    'status': 'healthy',
                    'message': 'Database connection successful',
                    'response_time_ms': 0  # Could measure actual response time
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}',
                'response_time_ms': None
            }
    
    @staticmethod
    def get_cache_status():
        """Check cache system status."""
        try:
            test_key = 'health_check_test'
            test_value = 'test_value'
            
            # Test cache write and read
            cache.set(test_key, test_value, 60)
            retrieved_value = cache.get(test_key)
            
            if retrieved_value == test_value:
                cache.delete(test_key)
                return {
                    'status': 'healthy',
                    'message': 'Cache system operational'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': 'Cache read/write test failed'
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Cache system error: {str(e)}'
            }
    
    @staticmethod
    def get_system_resources():
        """Get system resource usage."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            return {
                'status': 'healthy',
                'resources': {
                    'cpu': {
                        'usage_percent': cpu_percent,
                        'status': 'normal' if cpu_percent < 80 else 'high'
                    },
                    'memory': {
                        'total_gb': round(memory.total / (1024**3), 2),
                        'used_gb': round(memory.used / (1024**3), 2),
                        'usage_percent': memory.percent,
                        'status': 'normal' if memory.percent < 80 else 'high'
                    },
                    'disk': {
                        'total_gb': round(disk.total / (1024**3), 2),
                        'used_gb': round(disk.used / (1024**3), 2),
                        'usage_percent': round((disk.used / disk.total) * 100, 2),
                        'status': 'normal' if (disk.used / disk.total) < 0.8 else 'high'
                    }
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get system resources: {str(e)}'
            }
    
    @staticmethod
    def get_application_status():
        """Get application-specific status information."""
        try:
            from projects.models import Projeto
            from tasks.models import Tarefa
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            
            # Basic counts to verify database connectivity
            projects_count = Projeto.objects.count()
            tasks_count = Tarefa.objects.count()
            users_count = User.objects.count()
            
            return {
                'status': 'healthy',
                'application': {
                    'name': 'Planify API',
                    'version': '1.0.0',
                    'environment': getattr(settings, 'ENVIRONMENT', 'development'),
                    'debug_mode': settings.DEBUG,
                    'uptime': HealthService._get_uptime(),
                    'statistics': {
                        'projects': projects_count,
                        'tasks': tasks_count,
                        'users': users_count
                    }
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Application status check failed: {str(e)}'
            }
    
    @staticmethod
    def _get_uptime():
        """Calculate application uptime (simplified)."""
        try:
            # This is a simplified uptime calculation
            # In production, you might store startup time in a file or cache
            boot_time = psutil.boot_time()
            uptime_seconds = timezone.now().timestamp() - boot_time
            return {
                'seconds': int(uptime_seconds),
                'human_readable': str(timedelta(seconds=int(uptime_seconds)))
            }
        except:
            return {
                'seconds': 0,
                'human_readable': 'Unknown'
            }
    
    @staticmethod
    def get_comprehensive_health_check():
        """Perform comprehensive health check of all systems."""
        health_status = {
            'overall_status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'checks': {}
        }
        
        # Database check
        db_status = HealthService.get_database_status()
        health_status['checks']['database'] = db_status
        
        # Cache check
        cache_status = HealthService.get_cache_status()
        health_status['checks']['cache'] = cache_status
        
        # System resources
        system_status = HealthService.get_system_resources()
        health_status['checks']['system'] = system_status
        
        # Application status
        app_status = HealthService.get_application_status()
        health_status['checks']['application'] = app_status
        
        # Determine overall status
        unhealthy_checks = [
            check for check in health_status['checks'].values()
            if check.get('status') != 'healthy'
        ]
        
        if unhealthy_checks:
            health_status['overall_status'] = 'unhealthy'
            health_status['issues_count'] = len(unhealthy_checks)
        
        return health_status
