from django.urls import path, re_path
from . import views
#from .views import CustomerUpdateView

app_name = 'employees'

urlpatterns = [
    path('', views.show_all),
    path('animals/', views.employees_animals),
    path('add/', views.add_employee),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('search-result/', views.search_employees, name='search_employees'),

]
