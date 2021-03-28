from rest_framework.test import APITestCase
from api.models import Task
from api.serializers import TaskSerializer


class TasksApiTestCase(APITestCase):
    def test_list(self):
        task_1 = Task.objects.create(header='Test task 1', text='Testing', date='2020-06-10')
        task_2 = Task.objects.create(header='Test task 2', text='Testing', date='2020-06-10')

        url = '/api/tasks-list/'
        response = self.client.get(url)
        self.assertEqual(TaskSerializer([task_1, task_2], many=True).data, response.data['tasks'])

    def test_delete(self):
        task_1 = Task.objects.create(header='Test task 1', text='Testing', date='2020-06-10')

        url = '/api/delete-task/'
        self.client.delete(url + f'{task_1.id}/')
        self.assertEqual(Task.objects.count(), 0)

    def test_get(self):
        task_1 = Task.objects.create(header='Test task 1', text='Testing', date='2020-06-10')

        url = '/api/get-task/'
        response = self.client.get(url + f'{task_1.id}/')
        serializer = TaskSerializer(data=response.data['task'], many=False)
        if serializer.is_valid():
            self.assertEqual(serializer.data, TaskSerializer(task_1).data)

    def test_update(self):
        task_1 = Task.objects.create(header='Test task 1', text='Testing', date='2020-06-10', instance=False)
        task_1_copy = Task.objects.create(header='Test task 1', text='Testing',
                                          date='2020-06-10', instance=True)
        url = '/api/mark-as-done/'
        self.client.get(url + f'{task_1.id}/')
        task_1 = TaskSerializer(Task.objects.get(pk=f'{task_1.id}')).data
        self.assertEqual(TaskSerializer(task_1).data, TaskSerializer(task_1_copy).data)

    def test_post(self):
        task_1 = Task.objects.create(header='Test task 1', text='Testing', date='2020-06-10', instance=False)
        url = '/api/create-task/'
        self.client.post(url, data=TaskSerializer(task_1).data)
        self.assertEqual(Task.objects.count(), 2)

