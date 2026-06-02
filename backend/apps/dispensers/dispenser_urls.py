
"""
Router for dispenser API ViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import dispenser_views

app_name = 'dispensers'

# URLs manuales con tipos explícitos para evitar warnings de drf-spectacular
urlpatterns = [
    path('', dispenser_views.DispenserViewSet.as_view({'get': 'list', 'post': 'create'}), name='dispensers-list'),
    path('<str:pk>/', dispenser_views.DispenserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='dispensers-detail'),
    
    # Custom endpoints 
    path('get_total_spent_by_dispenser/<str:pk>/', dispenser_views.DispenserViewSet.as_view({'get': 'get_total_spent_by_dispenser'}), name='dispensers-get-total-spent-by-dispenser'),
]

