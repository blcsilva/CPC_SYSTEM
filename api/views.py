from rest_framework import generics, viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from .models import CustomUser, Campaign, UserTask, Payment, OfferCategory, Withdrawal
from .serializers import CustomUserSerializer, CampaignSerializer, UserTaskSerializer, PaymentSerializer, OfferCategorySerializer, WithdrawalSerializer

def home(request):
    return HttpResponse("Bem-vindo à API!")

class UserTaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # Exige autenticação

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

    def perform_update(self, serializer):
        # Atualiza a tarefa
        task = serializer.save()

        # Se a tarefa foi marcada como completada, registra o pagamento
        if task.completed and task.reward > 0:
            Payment.objects.create(user=task.user, amount=task.reward)

class UserTaskListCreateView(generics.ListCreateAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

class UserTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]  # Somente administradores podem gerenciar usuários

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]  # Apenas usuários autenticados podem acessar campanhas

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        amount = request.data.get('amount')
        if Payment.check_daily_limit(user, amount):
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "Daily limit exceeded"}, status=status.HTTP_400_BAD_REQUEST)

class OfferCategoryViewSet(viewsets.ModelViewSet):
    queryset = OfferCategory.objects.all()
    serializer_class = OfferCategorySerializer
    permission_classes = [IsAuthenticated]  # Somente usuários autenticados podem acessar

    def perform_create(self, serializer):
        serializer.save()

class WithdrawalViewSet(viewsets.ModelViewSet):
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]  # Exige autenticação

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)  # Lista apenas os saques do usuário autenticado

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data.get('amount')

        # Verifica se o valor mínimo de saque é atingido
        if amount < 10:  # Supondo que o valor mínimo para saque seja 10
            raise serializers.ValidationError("O valor mínimo para saque é 10.")

        # Verifica se o usuário tem saldo suficiente
        total_payments = Payment.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or 0

        if amount > total_payments:
            raise serializers.ValidationError("Saldo insuficiente para realizar este saque.")

        # Se as verificações passaram, salva a solicitação de saque associada ao usuário
        serializer.save(user=user)


