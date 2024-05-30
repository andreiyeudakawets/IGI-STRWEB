import logging
from calendar import HTMLCalendar
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import News, Review, Company
from .forms import ReviewForm
from employees.models import Customer, Employee
from tickets.models import Ticket, PromoCode

logging.basicConfig(level=logging.INFO, filename="webzoo.log")


def index(request):
    user_timezone = ''
    current_date = ''
    current_month = ''
    current_year = ''
    cal = ''
    month_number = ''
    us_gr = ''
    context = {}
    logging.info(f'Вызвана главная страница')

    if request.user.is_authenticated:
        user_timezone = timezone.get_current_timezone()
        current_date = timezone.localtime(timezone.now()).strftime('%d/%m/%Y')
        current_month = timezone.localtime(timezone.now()).month
        current_month = calendar.month_name[current_month]
        current_year = timezone.localtime(timezone.now()).year
        month_number = list(calendar.month_name).index(current_month)
        month_number = int(month_number)
        cal = HTMLCalendar().formatmonth(current_year, month_number)
        employee = None

        group = request.user.groups.all()
        if 'customer' in group.values_list('name', flat=True):
            customer = Customer.objects.get(user=request.user)
            num_rentals = Ticket.objects.filter(user=request.user).count()
            if num_rentals >= 3:
                customer.is_regular_customer = True
                customer.save()

        if request.user.groups.filter(name='worker').exists():
            us_gr = 'worker'
            #employee = Employee.objects.get(user=request.user)
        elif request.user.groups.filter(name='customer').exists():
            us_gr = 'customer'

        latest_news = News.objects.latest('time_create')

        context = {
            'current_month': current_month, 'current_year': current_year, 'cal': cal, 'month_number': month_number,
            'user_timezone': user_timezone, 'current_date': current_date, 'us_gr': us_gr, 'latest_news': latest_news
        }

    #logging.info(f"Вызвана главная страница")
    return render(request, 'mainapp/index.html', context)


def about(request):
    logging.info(f'Вызвана страница о сайте')
    company = Company.objects.get(name='Zoo')
    return render(request, 'mainapp/about.html', {'company': company})


def contact(request):
    logging.info(f'Вызвана страница контакты')
    return HttpResponse("Контакты")


def news(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    news = News.objects.all()
    logging.info(f"Вызвана страница новостей")
    return render(request, 'mainapp/news.html', {'news': news, 'us_gr': us_gr})


def codes(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    promocodes = PromoCode.objects.all()
    logging.info(f"Вызвана страница промокодов")
    return render(request, 'mainapp/codes.html', {'promocodes': promocodes, 'us_gr': us_gr})


def allreviews(request):
    logging.info(f"Вызвана страница отзывов")
    reviews = Review.objects.all()
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    return render(request, 'mainapp/reviews.html', {'reviews': reviews, 'us_gr': us_gr})



@login_required
def add_review(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            logging.info(f"Отзыв {review.id} добавлен")
            return redirect('/reviews/')
    else:
        form = ReviewForm()

    return render(request, 'mainapp/add_review.html', {'form': form, 'us_gr': us_gr})


def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('/reviews/')

def privacy(request):
    return HttpResponse('privacy')
