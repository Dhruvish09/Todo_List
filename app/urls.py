from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('', Generics_views.ListTodo.as_view(),name='get-todo'),
    path('create_todo', Generics_views.CreateTodo.as_view(),name='post-todo'),
    path('update_todo/<int:pk>', Generics_views.UpdateTodo.as_view(),name='update-todo'),
    path('delete_todo/<int:pk>', Generics_views.DeleteTodo.as_view(),name='delete-todo'),


    # API decorators Views 
    path('home', API_views.home,name='index'),
    path('create', API_views.post_todo,name='create'),
    path('update/<int:id>',API_views.put_todo,name='update'),
    path('partial_update/<int:id>',API_views.patch_todo,name='partial_update'),
    path('delete/<int:id>',API_views.delete_todo,name='delete_todo'),
   
   # API Views
    path('todo',API_views.TodoAPI.as_view()),
    path('todo/<int:pk>/',API_views.TodoAPI.as_view()),
    path('filter_search_todo',API_views.Filter_SearchTodo.as_view()),

    # Authentication
        #Jwt Default
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        
        #Jwt Manual
        path('register',UserAuthentication.UserRegister.as_view(),name="register"),
        path('login',UserAuthentication.UserLogin.as_view(),name="login"),
        path('profile',UserAuthentication.UserProfile.as_view(),name="profile"),
        path('logout',UserAuthentication.UserLogout.as_view(),name="logout"),
        path('change_password',UserAuthentication.UserChangePassword.as_view(),name="change_password")

]
