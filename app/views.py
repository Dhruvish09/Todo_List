from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    data = Todo.objects.all()
    context = {
       'data' : data,
    }
    return render(request,'crud.html',context)

def delete_todo(request,id):
    print("idddddd",id)
    try:
        print("333333333333333333")
        todo_id = Todo.objects.get(id=id)
        print(todo_id)
        todo_id.delete()
        print("Successssss")
        messages.success(request,"Your todo item deleted successfully")
    except Todo.DoesNotExist:
        print("Your todo item does not exist")
        messages.error(request,"Your todo item does not exist")
    except Exception as e:
        print("eeeeeeeeeeeee",e)
        messages.error(request,f"Fail operation because of: {str(e)}")

    return redirect('home')