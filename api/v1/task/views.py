from home.models import CustomUser, Task
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class AddTask(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskIsDeleted(generics.UpdateAPIView):
    serializer_class = TaskIsDeletedSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        return queryset

    def update(self, request, *args, **kwargs):
        data = {"is_deleted": True}

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {'message': 'Task updated successfully!'}
        return Response(response_data)   


class TaskIsDone(generics.UpdateAPIView):
    serializer_class = TaskIsDoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)

        return queryset

    def update(self, request, *args, **kwargs):

        data = {'is_done': True}

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
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
