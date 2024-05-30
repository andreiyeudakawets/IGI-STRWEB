from django.contrib import admin

from .models import Employee, EmployeePosition, Customer


admin.site.register(EmployeePosition)
admin.site.register(Employee)
admin.site.register(Customer)
