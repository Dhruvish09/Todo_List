from .models import *
from rest_framework import serializers
# from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        # Three ways to define fields for serializing data
        fields = '__all__'  #(1) Include all fields of the Todo model
        # fields = ['title','details']  #(2) Specify only 'title' and 'details' fields to include
        # exclude = ['id']  #(2) Exclude the 'id' field from serialization that means remove ID from serialize data.

    def validate(self, data):
        completed = data.get('completed', False)  # Defaulting to False if 'completed' is not present
        if completed:
            raise serializers.ValidationError({"Error": "Todo must be required in progress"})

        title = data.get('title', None)  # Safely retrieving 'title'
        if title is not None:
            if Todo.objects.filter(title=title).exists():
                raise serializers.ValidationError({"Error": "Title must be unique"})
        return data

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class Bookserializer(serializers.ModelSerializer):
    # category = Categoryserializer()
    class Meta:
        model = Book
        fields = '__all__'
    
class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password2'},write_only=True)
    class Meta:
        model = User
        fields = ('name', 'email','tc', 'password','password2')
        extra_kwargs = {
            'password':{'write_only':True}
            }

    def validate(self, attrs):
        password =attrs.get('password')
        password2 =attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and confirm password does't matched!")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['id','email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'})
    password2 = serializers.CharField(max_length=255, style={'input_type':'password2'})
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("Password and confirm password does't matched!")
        
        user.set_password(password)
        user.save()
        return attrs


