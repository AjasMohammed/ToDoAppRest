from home.models import CustomUser, Task
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class AddTask(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class UpdateTask(generics.UpdateAPIView):
    serializer_class = UpdateTaskSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        return queryset

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {'message': 'Task updated successfully!'}
        return Response(response_data)   

class ViewTask(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer


    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        return queryset
