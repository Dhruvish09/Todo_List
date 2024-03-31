from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework import status
from ..mypaginations import MyPagination
from rest_framework.filters import SearchFilter, OrderingFilter

class TodoAPI(APIView):
    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                todo = Todo.objects.get(id=pk)
                serializer = TodoSerializer(todo)
                return Response({"Status": status.HTTP_200_OK, "Payload": serializer.data})
            else:
                todo_objs = Todo.objects.all()
                serializer = TodoSerializer(todo_objs, many=True)
                return Response({"Status": status.HTTP_200_OK, "Payload": serializer.data})
        except Todo.DoesNotExist:
            return Response({"Status": status.HTTP_404_NOT_FOUND, "Message": "Todo object does not exist"})

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': status.HTTP_201_CREATED, 'Payload': serializer.data, 'Message': 'Data has been stored successfully'})
        else:
            return Response({'Status': status.HTTP_400_BAD_REQUEST, 'Error': serializer.errors})

    def put(self, request, pk, format=None):
        try:
            todo_obj = Todo.objects.get(pk=pk)
            serializer = TodoSerializer(todo_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Status': status.HTTP_200_OK, 'Payload': serializer.data, 'Message': 'Data has been Updated successfully'})
            else:
                return Response({'Status': status.HTTP_400_BAD_REQUEST, 'Error': serializer.errors, 'Message': 'Something went wrong'})
        except Todo.DoesNotExist:
            return Response({"Status": status.HTTP_404_NOT_FOUND, "Message": "Todo object does not exist"})

    def patch(self, request, pk, format=None):
        try:
            todo_obj = Todo.objects.get(pk=pk)
            serializer = TodoSerializer(todo_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Status': status.HTTP_200_OK, 'Payload': serializer.data, 'Message': 'Data has been partially updated successfully'})
            else:
                return Response({'Status': status.HTTP_400_BAD_REQUEST, 'Error': serializer.errors, 'Message': 'Something went wrong'})
        except Todo.DoesNotExist:
            return Response({"Status": status.HTTP_404_NOT_FOUND, "Message": "Todo object does not exist"})

    def delete(self, request, pk=None, format=None):
        try:
            if pk is None:
                return Response({"Status": status.HTTP_400_BAD_REQUEST, "Message": "Please provide a ID for delete your todo item"})
            else:
                todo_obj = Todo.objects.get(pk=pk)
                todo_obj.delete()
                return Response({"Status": status.HTTP_200_OK, "Message": "Item deleted successfully"})
        except Todo.DoesNotExist:
            return Response({"Status": status.HTTP_404_NOT_FOUND, "Message": "Todo object does not exist"})

class Filter_SearchTodo(APIView):
    pagination_class = MyPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get(self, request, format=None):
        queryset = Todo.objects.all()
        
        # Filtering
        search_filter = SearchFilter()
        queryset = search_filter.filter_queryset(request, queryset, self)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = TodoSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Serialize the queryset
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data)
     
# API VIEW Decorators

@api_view(['GET'])
def home(request):
    todo_objs = Todo.objects.all()
    serializer = TodoSerializer(todo_objs, many=True)
    return Response({'Status': status.HTTP_200_OK, 'Payload': serializer.data})

@api_view(['POST'])
def post_todo(request):
    data = request.data
    serializer = TodoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Status': status.HTTP_201_CREATED, 'Payload': serializer.data, 'Message': 'Data has been stored successfully'})
    else:
        return Response({'Status': status.HTTP_400_BAD_REQUEST, 'Error': serializer.errors})

@api_view(['PUT'])
def put_todo(request, id):
    try:
        todo_obj = Todo.objects.get(id=id)
        serializer = TodoSerializer(todo_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': status.HTTP_200_OK, 'Payload': serializer.data, 'Message': 'Data has been Updated successfully'})
        else:
            return Response({'Status': status.HTTP_400_BAD_REQUEST, 'Error': serializer.errors, 'Message': 'Something went wrong'})
    except Todo.DoesNotExist:
        return Response({"Status": status.HTTP_404_NOT_FOUND, "Message": "Todo object does not exist"})

@api_view(['PATCH'])
def patch_todo(request, id):
    try:
        todo_obj = Todo.objects.get(id=id)
        serializer = TodoSerializer(todo_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': status.HTTP_200_OK, 'Payload': serializer.data, 'Message': 'Data has been partially updated successfully'})
        else:
            return Response({'Status': status.HTTP_400_BAD_REQUEST, 'Error': serializer.errors, 'Message': 'Something went wrong'})
    except Todo.DoesNotExist:
        return Response({"Status": status.HTTP_404_NOT_FOUND, "Message": "Todo object does not exist"})

@api_view(['DELETE'])
def delete_todo(request, id):
    try:
        todo_obj = Todo.objects.get(id=id)
        todo_obj.delete()
        return Response({'Status': status.HTTP_200_OK, 'Message': 'Item deleted Successfully'})
    except Todo.DoesNotExist:
        return Response({'Status': status.HTTP_404_NOT_FOUND, 'Message': 'Todo object does not exist'})
    