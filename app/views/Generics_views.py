from django.shortcuts import render
from rest_framework import generics
from ..serializers import *
from ..models import Todo
from rest_framework.response import Response
from ..mypaginations import MyPagination
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

class ListTodo(generics.ListAPIView):   # List todo record
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = MyPagination
    
    filter_backends = [SearchFilter] #search filter
    search_fields = ['title']

    # filter_backends = [OrderingFilter] # Order filter
    # ordering_fields = ['id']

class CreateTodo(generics.CreateAPIView): # Create todo record
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class UpdateTodo(generics.RetrieveUpdateAPIView): # Update todo record
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class DeleteTodo(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

