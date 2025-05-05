from django.urls import path
from .views import (
    health_check,
    health_check_original,
    dashboard_overview,
    project_metrics,
    user_dashboard,
    api_documentation,
)

app_name = 'core'

urlpatterns = [
    path('', api_documentation, name='api-documentation'),
    path('health-check/', health_check, name='health-check'),
    path('health-check/original/', health_check_original, name='health-check-original'),
    path('dashboard/overview/', dashboard_overview, name='dashboard-overview'),
    path('dashboard/project/<int:project_id>/', project_metrics, name='project-metrics'),
    path('dashboard/user/', user_dashboard, name='user-dashboard'),
]
