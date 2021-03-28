from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('tasks-list/', views.taskList, name='task-list'),
    path('create-task/', views.taskCreate, name='create-task'),
    path('delete-task/<str:pk>/', views.taskDelete, name='delete-task'),
    path('mark-as-done/<str:pk>/', views.taskDone, name='change-an-instance'),
    path('get-task/<str:pk>/', views.taskGet, name='get-task')
]