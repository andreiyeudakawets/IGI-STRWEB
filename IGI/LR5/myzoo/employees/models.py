from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from rooms.models import Room


class EmployeePosition(models.Model):
    title = models.CharField(max_length=50)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=50, unique=True)
    age = models.PositiveIntegerField(default=18)
    position = models.ForeignKey(EmployeePosition, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='users_images', blank=True, null=True)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Customer(models.Model):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, unique=True)
    age = models.PositiveIntegerField(default=18)
    spendings = models.IntegerField(default=0, blank=True, null=True)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
