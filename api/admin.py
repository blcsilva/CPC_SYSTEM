from django.contrib import admin
from .models import CustomUser, Campaign, UserTask, Payment, PTOffer, UserPTOffer

# Registro do modelo CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_announcer', 'is_normal_user')
    search_fields = ('username', 'email')
    list_filter = ('is_admin', 'is_announcer', 'is_normal_user')

# Registro do modelo Campaign
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'start_date', 'end_date', 'budget')
    search_fields = ('title', 'description')
    list_filter = ('created_by', 'start_date', 'end_date')

# Registro do modelo UserTask
@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task_description', 'completed', 'created_at', 'reward')
    search_fields = ('user__username', 'task_description')
    list_filter = ('completed', 'created_at', 'user')

# Registro do modelo Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'created_at')
    search_fields = ('user__username', 'payment_method')
    list_filter = ('payment_method', 'created_at')

# Registro do modelo PTOffer
@admin.register(PTOffer)
class PTOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'reward', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

# Registro do modelo UserPTOffer
@admin.register(UserPTOffer)
class UserPTOfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'pt_offer', 'participation_date', 'completed')
    search_fields = ('user__username',)
    list_filter = ('completed', 'participation_date')

