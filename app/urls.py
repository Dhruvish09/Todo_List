
from django.urls import path,include
from app import views 

urlpatterns = [
    path('',views.home, name='home'),
    path('todo',views.todo, name='todo'),
    path('add_todo',views.add_todo,name='add_todo'),
    path('update_todo/<int:todo_id>', views.update_todo, name='update_todo'),
    path('delete_todo/<int:id>',views.delete_todo, name='delete_todo'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name="signup"),
    path('logout',views.logout,name='logout')
]
