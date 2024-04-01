
from django.urls import path,include
from app import views 

urlpatterns = [
    path('index',views.index, name='home'),
    path('delete_todo/<int:id>',views.delete_todo, name='delete_todo'),
]
