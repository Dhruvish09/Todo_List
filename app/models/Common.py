from django.db import models
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=150, blank=False)
    date = models.DateField(blank=True)
    details = models.CharField(max_length=250) 
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
class Category(models.Model):
    title = models.CharField(max_length=150)
    
    def __str__(self):
        return self.title
    
class Book(models.Model):
    title = models.CharField(max_length=150, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


