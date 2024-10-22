from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import CustomUser, Campaign, UserTask, Payment
from .serializers import CustomUserSerializer, CampaignSerializer, UserTaskSerializer, PaymentSerializer


def home(request):
    return HttpResponse("Bem-vindo à API!")


class UserTaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação para todas as ações

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return UserTask.objects.all()  # O administrador vê todas as tarefas
        elif user.is_announcer:
            return UserTask.objects.filter(user=user)  # O anunciador vê apenas suas próprias tarefas
        return UserTask.objects.none()  # Outros usuários não podem ver tarefas

    def perform_create(self, serializer):
        # As tarefas são criadas associadas ao usuário autenticado
        serializer.save(user=self.request.user)


# View para listar e criar tarefas (pode ser removida se já estiver implementada no UserTaskViewSet)
class UserTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return UserTask.objects.all()  # O administrador vê todas as tarefas
        elif user.is_announcer:
            return UserTask.objects.filter(user=user)  # O anunciador vê apenas suas próprias tarefas
        return UserTask.objects.none()  # Outros usuários não podem ver tarefas


# View para detalhar, atualizar ou deletar uma tarefa específica
class UserTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return UserTask.objects.all()  # O administrador vê todas as tarefas
        elif user.is_announcer:
            return UserTask.objects.filter(user=user)  # O anunciador vê apenas suas próprias tarefas
        return UserTask.objects.none()  # Outros usuários não podem ver tarefas


# View para gerenciar usuários
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]  # Somente administradores podem gerenciar usuários


# View para gerenciar campanhas
class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]  # Apenas usuários autenticados podem acessar campanhas

    def get_queryset(self):
        return Campaign.objects.all()  # Todos os usuários autenticados podem ver todas as campanhas

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# View para gerenciar pagamentos
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Apenas usuários autenticados podem acessar pagamentos

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
