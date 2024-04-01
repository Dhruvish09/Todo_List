from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from .form import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.


def index(request):
    data = Todo.objects.all()

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
            form.save()
            title = form.cleaned_data['title']
            messages.success(request, f"Todo <strong>{title}</strong> added successfully.")
            return redirect('index')
        else:
            for field, error_messages in form.errors.items():
                error_message = error_messages[0]
                messages.error(request, error_message)
            return redirect('index')
    else:
        form = TodoForm()
    return render(request, "index.html", {'form': form})

def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    print("todo",todo)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        print("form_error",form.errors)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            messages.success(request, f"Todo <strong>{title}</strong> updated successfully.")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label
                    error_message = f"{field_label}: {error}"
                    messages.error(request, error_message)
                return redirect('index')
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

    return redirect('index')