from django.db import models
from django.contrib.auth.models import AbstractUser

# Crie um modelo de usuário personalizado
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_announcer = models.BooleanField(default=False)
    is_normal_user = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Altere para evitar conflito
        blank=True,
        help_text='Os grupos aos quais este usuário pertence. Um usuário receberá todas as permissões concedidas a cada um de seus grupos.',
        verbose_name='grupos',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Altere para evitar conflito
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='permissões de usuário',
    )

    def __str__(self):
        return self.username


# Modelo para campanhas publicitárias
class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, default="Descrição padrão")  # Permite nulos
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='campaigns', null=True)  # Permite nulos

    def __str__(self):
        return self.title


# Modelo para tarefas do usuário
class UserTask(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    task_description = models.TextField(null=True, default="Descrição padrão")  # Permite nulos
    reward = models.DecimalField(max_digits=10, decimal_places=2)  # Mantendo o termo 'reward' para clareza
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Task for {self.user.username}: {self.task_description}'


# Modelo para pagamentos
class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  # Ex: 'PayPal', 'Stripe', etc.

    def __str__(self):
        return f'Payment of {self.amount} for {self.user.username}'
