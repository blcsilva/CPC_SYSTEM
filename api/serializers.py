from rest_framework import serializers
from .models import CustomUser, Campaign, UserTask, Payment

# Serializer para o modelo CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_admin', 'is_announcer', 'is_normal_user', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Esconde a senha na representação do objeto

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hashing da senha
        user.save()
        return user

# Serializer para o modelo Campaign
class CampaignSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)  # Mostra o username do criador da campanha

    class Meta:
        model = Campaign
        fields = ('id', 'title', 'description', 'budget', 'start_date', 'end_date', 'created_by')

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError("O orçamento deve ser um valor positivo.")
        return value

# Serializer para o modelo UserTask
class UserTaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Mostra o username do usuário associado

    class Meta:
        model = UserTask
        fields = ('id', 'user', 'task_description', 'reward', 'completed', 'created_at')

    def validate_earnings(self, value):
        if value < 0:
            raise serializers.ValidationError("Os ganhos não podem ser negativos.")
        return value

# Serializer para o modelo Payment
class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Mostra o username do usuário associado

    class Meta:
        model = Payment
        fields = ('id', 'user', 'amount', 'created_at', 'payment_method')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor do pagamento deve ser um valor positivo.")
        return value
