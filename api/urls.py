from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home,  # Importando a função home
    UserTaskListCreateView,
    UserTaskDetailView,
    CustomUserViewSet,
    CampaignViewSet,
    PaymentViewSet,
)

# Configurando o roteador para os viewsets
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', home, name='home'),  # Home da API
    path('tasks/', UserTaskListCreateView.as_view(), name='user-task-list-create'),
    path('tasks/<int:pk>/', UserTaskDetailView.as_view(), name='user-task-detail'),
    path('', include(router.urls)),  # Inclui as rotas do router para os viewsets
]
