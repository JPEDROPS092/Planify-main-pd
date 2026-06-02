"""Rotas do app ``customers`` (montadas sob ``/api/``).

- ``/api/tenant/invitations/``: gestão de convites (owner/admin do tenant).
- ``/api/invitations/<token>/`` e ``/api/invitations/<token>/accept/``: rotas
  públicas de inspeção e aceite de convite.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    InvitationAcceptView,
    InvitationDetailView,
    TenantInvitationViewSet,
)

app_name = 'customers'

router = DefaultRouter()
router.register(r'tenant/invitations', TenantInvitationViewSet, basename='tenant-invitation')

urlpatterns = [
    path('', include(router.urls)),
    path('invitations/<str:token>/', InvitationDetailView.as_view(), name='invitation-detail'),
    path('invitations/<str:token>/accept/', InvitationAcceptView.as_view(), name='invitation-accept'),
]
