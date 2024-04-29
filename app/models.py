from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):

    LOW = 'Low'
    MIDDLE = 'Middle'
    HIGH = 'High'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MIDDLE, 'Middle'),
        (HIGH, 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', default='', null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default = False)

    def __str__(self):
        return self.title
