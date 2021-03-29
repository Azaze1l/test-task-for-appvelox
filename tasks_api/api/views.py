from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from rest_framework import status
import copy
from .services.error_catcher import protected_view


@protected_view
@api_view(['GET'])
def apiOverview(request):
    """
    Функция, предоставляющая опции данного API
    """
    api_endpoints = {
        'List': '/tasks-list/',
        'Create': '/create_task/',
        'Get': '/get-task/',
        'Update': '/mark-as-done/',
        'Delete': '/delete-task/'
    }
    return Response(api_endpoints)


@protected_view
@api_view(['GET'])
def taskList(request):
    """
    Функция, отображающая список существующих в БД документов (в терминологии MongoDB)
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response({'tasks': serializer.data})


@protected_view
@api_view(['POST'])
def taskCreate(request):
    """
    Функция, валидирующая входные данные о новой задаче и создающая ее
    """
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Task is successfully created'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)


@protected_view
@api_view(['DELETE'])
def taskDelete(request, pk):
    """
    Функция, удаляющая документ с задачей из базы данных по переданному primary key
    """
    try:
        task = Task.objects.get(id=pk)
        task.delete()
        return Response({'message': 'Task is successfully deleted'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)


@protected_view
@api_view(['GET'])
def taskGet(request, pk):
    """
    Функция, возвращающая информацию о существующей в бд задаче по переданному primary key
    """
    try:
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task, many=False)
        return Response({'task': serializer.data}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)


@protected_view
@api_view(['GET'])
def taskDone(request, pk):
    """
    Функция, отмечающая задачу как "выполненная" по определенному primary key
    """
    task = Task.objects.get(id=pk)
    updated_task = copy.deepcopy(task)
    updated_task.instance = True
    serializer = TaskSerializer(instance=task, data=TaskSerializer(updated_task).data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Task is marked as done'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
