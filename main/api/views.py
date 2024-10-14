from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, When
from django.shortcuts import get_object_or_404
from main.models import Task
from .serializers import TaskSerializer
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
def home(request):
    return Response({'message': 'Welcome to the Task Management API!'}, status=status.HTTP_200_OK)

class TaskList(APIView):
    authentication_classes = [JWTAuthentication]  # Require JWT authentication
    permission_classes = [IsAuthenticated]  # Require authentication


    def get_queryset(self, user, **kwargs):
        """Return filtered queryset based on the user."""
        return Task.objects.filter(user=user, **kwargs)  # Assuming Task has a ForeignKey to User

    def get(self, request):
        """Retrieve tasks for the authenticated user."""
        params = {key: value for key, value in request.query_params.items() if value and key != 'sort_by'}

        sort_by = request.query_params.get('sort_by')
        valid_sort_fields = ['created_at', 'due_date', 'priority']

        tasks = self.get_queryset(request.user, **params)  # Filter by logged-in user

        if sort_by == 'priority':
            tasks = tasks.annotate(
                priority_order=Case(
                    When(priority='high', then=1),
                    When(priority='medium', then=2),
                    When(priority='low', then=3),
                    output_field=models.IntegerField(),
                )
            ).order_by('priority_order')
        elif sort_by in valid_sort_fields:
            tasks = tasks.order_by(sort_by)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new task for the authenticated user."""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the user to the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

# TaskDetail class with get_object method
class TaskDetail(APIView):
    authentication_classes = [JWTAuthentication]  # Require JWT authentication
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_object(self, pk):
        # Simplify this method with get_object_or_404
        task = get_object_or_404(Task, pk=pk)
        # Ensure the task belongs to the authenticated user
        if task.user != self.request.user:
            # If the task does not belong to the user, raise a 403 Forbidden error
            return None
        return task

    def get(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)