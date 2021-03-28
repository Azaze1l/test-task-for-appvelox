from api.models import Task
from api.serializers import TaskSerializer
from django.test import TestCase


class SerializersTest(TestCase):
    def test_task_serializer(self):
        task_1 = Task.objects.create(header='Test task 1', text='Testing', date='2020-06-10')

        data = TaskSerializer(task_1).data
        expected_data = {
            'header': task_1.header,
            'text': task_1.text,
            'date': task_1.date,
            'instance': False
        }
        self.assertEqual(data, expected_data)