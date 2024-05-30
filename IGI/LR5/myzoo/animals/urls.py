from django.urls import path, re_path
from . import views

app_name = 'animals'

urlpatterns = [
    path('', views.animal_list, name='allanimals'),
    path('animal_family_population/', views.animal_family_population),
    path('add/', views.add_animal, name='add_animal'),
    path('sort/', views.sort_animals, name='sort_animals'),
    path('search-result/', views.search_animals, name='search_animals'),
    path('delete/<int:id>/', views.delete_animal, name='delete_animal'),
    path('edit/<int:id>/', views.edit_animal, name='change_animal'),
]
