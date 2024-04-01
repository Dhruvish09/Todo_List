from django.forms import ModelForm
from .models import *

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
