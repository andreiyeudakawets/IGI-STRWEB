from django.utils import timezone
from django.db import models


class Room(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=50)
    pond = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    image = models.ImageField(upload_to='rooms_images', blank=True, null=True)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)
    #employees = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
