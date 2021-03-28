from djongo import models


class Task(models.Model):
    header = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateField(default=None)
    instance = models.BooleanField(default=False, blank=True)

