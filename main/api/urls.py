from django.urls import path

from .views import home, TaskList, TaskDetail
from .authentication import RegisterView, LoginView

urlpatterns = [
    path('', home, name='home'),
    path('tasks/', TaskList.as_view(), name='task-list'), # GET, POST
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'), # GET, PUT, DELETE
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
]