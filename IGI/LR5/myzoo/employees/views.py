import logging

from django.contrib.auth import authenticate
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Customer, Employee
from animals.models import Animal
from animals.forms import AnimalForm
from .forms import EmployeeChangeForm, EmployeePositionForm, EmployeeCreationForm

logging.basicConfig(level=logging.INFO, filename="webzoo.log")


def show_all(request):
    logging.info(f'Вызвана страница всех работников')
    #current_date = ''
    current_date = timezone.localtime(timezone.now()).strftime('%d/%m/%Y')
    employees = Employee.objects.all()
    return render(request, 'employees/showall.html', {'employees': employees, 'current_date': current_date})


def search_employees(request):
    logging.info(f'Вызвана функция поиска работников')
    if request.method == 'GET':
        search_query = request.GET.get('q')

        if search_query:
            employees = Employee.objects.filter(room__title__icontains=search_query)
        else:
            employees = Employee.objects.all()

        return render(request, 'employees/showall.html', {'employees': employees, 'search_query': search_query})

    return redirect('/employees/')


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            #login(request, user)
            logging.info(f'Работник удален')
            return redirect('/employees/')
        else:
            logging.warning(f'Form isnt valid')
    else:
        form = EmployeeCreationForm()
    return render(request, 'employees/add_employee.html', {'form': form})


def delete_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        logging.info(f'Работник {employee.id} удален')
        return redirect("/employees/")
    except Employee.DoesNotExist:
        return HttpResponseNotFound("<h2>Employee not found</h2>")


def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = EmployeeChangeForm(data=request.POST, instance=employee.user, files=request.FILES)
        pos_form = EmployeePositionForm(data=request.POST, instance=employee.position)
        if form.is_valid():
            form.save()
            pos_form.save()
            logging.info(f'Работник {employee.id} изменен')
            return redirect('/employees/')
        else:
            logging.warning(f'Form isnt valid')
    else:
        form = EmployeeChangeForm(instance=employee.user)
        pos_form = EmployeePositionForm(instance=employee.position)
    context = {
        'form': form,
        'pos_form': pos_form,
        'employee': employee,
    }
    return render(request, 'employees/edit_employee.html', context)


def employees_animals(request):
    logging.info(f'Вызвана страница животных работника')
    us_gr = 'worker'
    employee = Employee.objects.get(user=request.user)
    animals = Animal.objects.filter(responsible_employee=employee)

    return render(request, 'employees/showanimals.html', {'animals': animals, 'us_gr': us_gr})
