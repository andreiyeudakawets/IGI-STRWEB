from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, DateForm, PromoCodeForm
from .models import Ticket, Discount, PromoCode
from employees.models import Customer
import logging

logging.basicConfig(level=logging.INFO, filename="webzoo.log")


def is_first(user):
    tickets = Ticket.objects.filter(user=user)
    if len(tickets) == 0:
        return True
    else:
        return False


def is_regular(user):
    tickets = Ticket.objects.filter(user=user)
    if len(tickets) > 5:
        return True
    else:
        return False


@login_required
def buy_ticket(request):
    form = TicketForm(request.POST or None)
    price = None

    if request.method == 'POST' and 'check_price' in request.POST:
        if form.is_valid():
            form.set_ticket_price()
            weekday = form.cleaned_data.get('weekday')
            if weekday < date.today():
                form.add_error('rental_date', 'Выберите дату, большую или равную текущей дате.')
                return render(request, 'tickets/buy_tickets.html', {'form': form})
            # Calculate the price based on the selected weekday
            if weekday.weekday() in [0, 1, 2, 3, 4]:  # Monday, Tuesday, Wednesday...
                form.instance.price = 10
            else:
                form.instance.price = 15

            total_price = form.instance.price
            price = total_price
            discount_percent_promo = 0

            if form.cleaned_data['promocode']:
                try:
                    promo_code = PromoCode.objects.get(code=form.cleaned_data['promocode'])
                    discount_percent_promo = promo_code.discount_percentage
                    discounted_price = total_price - (total_price * discount_percent_promo / 100)
                    price = discounted_price
                except PromoCode.DoesNotExist:
                    form.add_error('promocode', 'Промокод не найден.')
                    return render(request, 'tickets/buy_tickets.html', {'form': form})
            if is_first(request.user):
                try:
                    discount = Discount.objects.get(name='Первая покупка')
                    discount_percent = discount.percentage
                    all_discount = discount_percent + discount_percent_promo
                    discounted_price = total_price - (total_price * all_discount / 100)
                    price = discounted_price
                except Discount.DoesNotExist:
                    return HttpResponse("Ошибка")
            elif is_regular(request.user):
                try:
                    discount = Discount.objects.get(name='Постоянный клиент')
                    discount_percent = discount.percentage
                    all_discount = discount_percent + discount_percent_promo
                    discounted_price = total_price - (total_price * all_discount / 100)
                    price = discounted_price
                except Discount.DoesNotExist:
                    return HttpResponse("Ошибка")
            else:
                price = total_price - (total_price * discount_percent_promo / 100)
            price = int(price)

    elif request.method == 'POST' and 'buy' in request.POST:
        if form.is_valid():
            form.set_ticket_price()

            weekday = form.cleaned_data.get('weekday')
            if weekday < date.today():
                form.add_error('weekday', 'Выберите дату, большую или равную текущей дате.')
                return render(request, 'tickets/buy_tickets.html', {'form': form})
            # Calculate the price based on the selected weekday
            if weekday.weekday() in [0, 1, 2, 3, 4]:  # Monday, Tuesday, Wednesday...
                form.instance.price = 10
            else:
                form.instance.price = 15

            ticket = form.save(commit=False)
            total_price = ticket.price
            ticket.user = request.user
            discount_percent_promo = 0

            if form.cleaned_data['promocode']:
                try:
                    promo_code = PromoCode.objects.get(code=form.cleaned_data['promocode'])
                    discount_percent_promo = promo_code.discount_percentage
                    discounted_price = total_price - (total_price * discount_percent_promo / 100)
                    ticket.price = discounted_price
                    ticket.promocode = promo_code
                    ticket.save()

                except PromoCode.DoesNotExist:
                    form.add_error('promocode', 'Промокод не найден.')
                    return render(request, 'tickets/buy_tickets.html', {'form': form})
            if is_first(request.user):
                try:
                    discount = Discount.objects.get(name='Первая покупка')
                    discount_percent = discount.percentage
                    all_discount = discount_percent + discount_percent_promo
                    discounted_price = total_price - (total_price * all_discount / 100)
                    ticket.price = discounted_price
                    ticket.discount = discount
                    ticket.save()
                except Discount.DoesNotExist:
                    ticket.save()
                    #promocode = form.cleaned_data['promocode']
            elif is_regular(request.user):
                try:
                    discount = Discount.objects.get(name='Постоянный клиент')
                    discount_percent = discount.percentage
                    all_discount = discount_percent + discount_percent_promo
                    discounted_price = total_price - (total_price * all_discount / 100)
                    ticket.price = discounted_price
                    ticket.discount = discount
                    ticket.save()
                except Discount.DoesNotExist:
                    ticket.save()
            else:
                ticket.price = total_price - (total_price * discount_percent_promo / 100)

            logging.info(f"Билет {ticket.id} куплен {ticket.user.username}")
            ticket.save()
            return redirect('/animals/')

    return render(request, 'tickets/buy_tickets.html', {'form': form, 'price': price})


@login_required
def user_tickets(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    tickets = Ticket.objects.filter(user=request.user).order_by('-weekday')
    logging.info(f"Вызвана страница билетов юзера")
    return render(request, 'tickets/user_tickets.html', {'tickets': tickets, 'us_gr': us_gr})


def ticket_list(request):
    form = TicketForm(request.POST or None)
    price = None

    if request.method == 'POST' and 'check_price' in request.POST:
        if form.is_valid():
            form.set_ticket_price()
            price = form.instance.price

    elif request.method == 'POST' and 'ok' in request.POST:
        if form.is_valid():
            return redirect('/animals/')  # Перенаправление на страницу успешной покупки билета

    return render(request, 'tickets/tickets_list.html', {'form': form, 'price': price})


def list_codes(request):
    codes = PromoCode.objects.all()
    logging.info(f"Вызвана страница всех промокодов")
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    return render(request, 'tickets/allcodes.html', {'codes': codes, 'us_gr': us_gr})


def delete_code(request, code_id):
    code = get_object_or_404(PromoCode, id=code_id)
    logging.info(f"Код {code} удален")
    code.delete()
    return redirect('/tickets/all-codes/')


def add_code(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            percent = form.cleaned_data['discount_percentage']
            if percent >= 100:
                logging.error(f'Discount percentage > 100')
                return HttpResponse('Discount percentage error')
            form.save()
            logging.info(f"Новый промокод добавлен")
            return redirect('/tickets/all-codes/')
        else:
            logging.warning(f'Form is not valid')
    else:
        form = PromoCodeForm()
    return render(request, 'tickets/add_promo.html', {'form': form, 'us_gr': us_gr})


def edit_code(request, code_id):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    code = get_object_or_404(PromoCode, id=code_id)
    if request.method == 'POST':
        form = PromoCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            logging.info(f"Промокод изменен")
            return redirect('/tickets/all-codes')
        else:
            logging.warning(f'Form is not valid')
    else:
        form = PromoCodeForm(instance=code)
    return render(request, "tickets/add_promo.html", {'form': form, 'us_gr': us_gr})

