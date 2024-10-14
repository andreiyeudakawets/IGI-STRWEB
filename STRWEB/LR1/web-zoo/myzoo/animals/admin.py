from django.contrib import admin

from .models import Country, Animal, AnimalClass

admin.site.register(Country)
admin.site.register(Animal)
admin.site.register(AnimalClass)
