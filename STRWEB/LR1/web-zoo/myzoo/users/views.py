import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .forms import CustomerChangeForm, CustomerCreationForm
from tickets.models import Ticket

from employees.models import Customer
from employees.models import Employee
import plotly.graph_objects as go
from statistics import mode, median, mean

logging.basicConfig(level=logging.INFO, filename="webzoo.log")


def register(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            logging.info(f'Юзер {user.id} зарегистрирован')
            return redirect('/animals/')
    else:
        form = CustomerCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logging.info(f'Юзер {user.id} вошел')
                return redirect('/animals/')
            else:
                logging.warning(f'Form isnt valid')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    #messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    logout(request)
    logging.info(f'Юзер {request.user.id} вышел')
    return redirect('/animals/')


@login_required
def user_profile(request):
    #user = request.user

    if request.method == 'POST':
        form = CustomerChangeForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            logging.info(f'Юзер {request.user.id} изменен')
            return redirect('/animals/')
        else:
            logging.warning(f'Form isnt valid')
    else:
        form = CustomerChangeForm(instance=request.user)

    groups = request.user.groups.all()

    if 'customer' in groups.values_list('name', flat=True):
        usr = Customer.objects.get(user=request.user)
    elif 'worker' in groups.values_list('name', flat=True):
        usr = Employee.objects.get(user=request.user)

    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    context = {'form': form, 'customer': usr, 'groups': groups, 'us_gr': us_gr}
    return render(request, 'users/profile.html', context)


def delete_user(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        if customer:
            user = customer.user
            customer.delete()
            user.delete()
            logging.info(f'Юзер {user.id} удален')
        return redirect("/user/customers/")
    except Customer.DoesNotExist:
        logging.error(f'Customer not found')
        return HttpResponseNotFound("<h2>Customer not found</h2>")


def customers_list(request):
    us_gr = ''
    customers = Customer.objects.all()
    total = 0
    logging.info(f'Вызвана страница всех клиентов')
    for customer in customers:
        customer.spendings = 0
        tickets = Ticket.objects.filter(user=customer.user)
        for ticket in tickets:
            customer.spendings += ticket.price
        total += customer.spendings
        customer.save()

    customer_spendings = [customer.spendings for customer in customers]
    all_names = [customer.user.username for customer in customers]
    fig = go.Figure(data=[go.Bar(x=all_names, y=customer_spendings)])

    fig.update_layout(
        title="All incomes",
        xaxis_title="Users",
        yaxis_title="Amount"
    )

    plot_div = fig.to_html(full_html=False)

    #list = Ticket.objects.values_list('price', flat=True)
    #spendings_mode = mode(list)

    spendings_list = Customer.objects.values_list('spendings', flat=True)
    spendings_mode = mode(spendings_list)
    spendings_median = median(spendings_list)
    spendings_mean = mean(spendings_list)


    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    context = {
        'customers': customers, 'us_gr': us_gr, 'total': total,
        'plot_div': plot_div, 'spendings_mode': spendings_mode,
        'spendings_median': spendings_median, 'spendings_mean': spendings_mean
    }

    return render(request, 'users/customers.html', context)


class CustomerUpdateView(UpdateView):
    model = User

    form_class = CustomerChangeForm
    template_name = 'users/profile.html'
    success_url = '/animals/'  # URL, куда перенаправить после успешного обновления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        customer = Customer.objects.get(user=user)
        context['customer'] = customer
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Получаем объект User, который был обновлен
        user = self.object

        # Обновляем соответствующий объект Customer
        customer = Customer.objects.get(user=user)
        customer.phone_number = form.cleaned_data['phone_number']
        customer.image = form.cleaned_data['image']
        customer.save()

        return response
