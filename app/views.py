from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages,auth
from .form import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app.decorators import auth_user_should_not_access
# Create your views here.

@auth_user_should_not_access
def home(request):
    return render(request, "index.html")

@login_required(login_url="signin")
def todo(request):
    data = Todo.objects.filter(user__id=request.user.id)

    page = request.GET.get('page',1)
    paginator = Paginator(data, 4)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
       'data' : data,
    }
    return render(request,'crud.html',context)

def add_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            title = form.cleaned_data['title']
            messages.success(request, f"Todo <strong>{title}</strong> added successfully.")
            return redirect('todo')
        else:
            for field, error_messages in form.errors.items():
                error_message = error_messages[0]
                messages.error(request, error_message)
            return redirect('todo')
    else:
        form = TodoForm()
    return render(request, "crud.html", {'form': form})

def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            messages.success(request, f"Todo <strong>{title}</strong> updated successfully.")
            return redirect('todo')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label
                    error_message = f"{field_label}: {error}"
                    messages.error(request, error_message)
                return redirect('todo')
    else:
        form = TodoForm(instance=todo)
    return render(request, "crud.html", {'form': form})

def delete_todo(request,id):
    print(id)
    try:
        todo_id = Todo.objects.get(id=id)
        todo_id.delete()
        messages.success(request,"Your todo item deleted successfully")
    except Todo.DoesNotExist:
        messages.error(request,"Your todo item does not exist")
    except Exception as e:
        messages.error(request,f"Fail operation because of: {str(e)}")

    return redirect('todo')

def signin(request):
    if request.method == "POST":
        form_error = False
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                
                # Store user information in session
                request.session['username'] = user.username
                request.session['user_id'] = user.id
                # You can store more information in the session as needed
                
                list(messages.get_messages(request))
                messages.success(request, f"Hello <strong>{request.user.username}</strong> You have been logged in")
                return redirect('todo')
        else:
            form_error = True
            for key, msg in list(form.errors.items()):
                error_message =  list(msg)
                messages.error(request, error_message[0])
                return redirect('/')

    form = UserLoginForm()

    return render(request,'index.html',{'form':form})


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,f"User {user.username} created successfully.")
            return redirect('todo')
        else:
            for key, msg in list(form.errors.items()):
                error_message =  list(msg)
                messages.error(request, error_message[0])
            return redirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'index.html', {'form': form})

def logout(request):
    user = request.user.username
    request.session.clear()
    auth.logout(request)
    list(messages.get_messages(request))
    messages.success(request, f"Dear user {user}, you have been logged out successfully.")
    return redirect('home')