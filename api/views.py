from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import CustomUser, Campaign, UserTask, Payment
from .serializers import CustomUserSerializer, CampaignSerializer, UserTaskSerializer, PaymentSerializer




def home(request):
    return HttpResponse("Bem-vindo à API!")

# View para listar e criar tarefas
class UserTaskListCreateView(generics.ListCreateAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

# View para detalhar, atualizar ou deletar uma tarefa específica
class UserTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

# View para gerenciar usuários
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]  # Somente administradores podem gerenciar usuários

# View para gerenciar campanhas
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]  # Apenas usuários autenticados podem acessar campanhas

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# View para gerenciar pagamentos
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Apenas usuários autenticados podem acessar pagamentos

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
