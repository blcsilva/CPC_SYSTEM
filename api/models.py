from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    completed = models.BooleanField(default=False)

class Campaign(models.Model):
    advertiser = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
