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
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Altere para evitar conflito
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
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
    reward = models.DecimalField(max_digits=10, decimal_places=2)  # Mantendo o termo 'reward' para claridade
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


class OfferCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class PTOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(OfferCategory, on_delete=models.CASCADE, related_name='offers', null=True)
    
    class Meta:
        verbose_name = "Oferta PTC"
        verbose_name_plural = "Ofertas PTC"

    def __str__(self):
        return self.title


# Modelo para registrar a participação do usuário nas ofertas PTC
class UserPTOffer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_pt_offers')  # Usuário que participou da oferta
    pt_offer = models.ForeignKey(PTOffer, on_delete=models.CASCADE, related_name='user_participations')  # Oferta PTC associada
    participation_date = models.DateTimeField(auto_now_add=True)  # Data de participação
    completed = models.BooleanField(default=False)  # Indica se a oferta foi completada

    class Meta:
        verbose_name = "Participação na Oferta PTC"
        verbose_name_plural = "Participações nas Ofertas PTC"

    def __str__(self):
        return f"{self.user.username} - {self.pt_offer.title}"
    
    
class Withdrawal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    
    def __str__(self):
        return f'Withdrawal of {self.amount} for {self.user.username}'