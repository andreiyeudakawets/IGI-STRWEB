from django.db import models
from django.urls import reverse
from django.utils import timezone

from employees.models import Employee


class Country(models.Model):
    name = models.CharField(max_length=50)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class AnimalClass(models.Model):
    name = models.CharField(max_length=50, unique=True)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Класс животных'
        verbose_name_plural = 'Классы животных'

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, help_text="female/male")
    age = models.PositiveIntegerField()
    country = models.ManyToManyField(Country)
    amount_of_feed = models.PositiveIntegerField(help_text="per day (g)")
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.CASCADE, null=True, related_name='animals')
    image = models.ImageField(upload_to='animals_images', blank=True, null=True)

    responsible_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

    def __str__(self):
        return self.name
