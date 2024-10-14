import logging
import re
from calendar import HTMLCalendar
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import News, Review, Company, FAQEntry, Vacancy, Product, Cart, Partner
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

    partners = Partner.objects.all()
    partners_dict = {'partners': partners}
    context.update(partners_dict)

    return render(request, 'mainapp/index.html', context)


def about(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    logging.info(f'Вызвана страница о сайте')
    company = Company.objects.get(name='Zoo')
    return render(request, 'mainapp/about.html', {'company': company, 'us_gr': us_gr})


def contact(request):
    logging.info(f'Вызвана страница контакты')
    return HttpResponse("Контакты")

def get_first_sentence(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences[0] if sentences else ''

def news(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    news = News.objects.all()

    for new in news:
        new.summary = get_first_sentence(new.content)
    logging.info(f"Вызвана страница новостей")
    return render(request, 'mainapp/news/news.html', {'news': news, 'us_gr': us_gr})


def get_news(request, id):
    news = News.objects.get(id=id)
    return render(request, 'mainapp/news/getnews.html', {'news': news})


def questions(request):
    questions = FAQEntry.objects.all()
    return render(request, 'mainapp/faq/questions.html', {'questions': questions})

"""
def answers(request, id):
    faqs = FAQEntry.objects.get(id=id)
    return render(request, 'mainapp/faq/answer.html', {'faqs': faqs})
"""


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
    return render(request, 'mainapp/reviews/reviews.html', {'reviews': reviews, 'us_gr': us_gr})



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
            review.rating = request.POST.get('rating')
            review.text = request.POST.get('text')
            review.save()
            logging.info(f"Отзыв {review.id} добавлен")
            return redirect('/reviews')
    else:
        form = ReviewForm()

    return render(request, 'mainapp/reviews/add_review.html', {'form': form, 'us_gr': us_gr})


def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('/reviews')

def privacy(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    return render(request, 'mainapp/privacy.html', {'us_gr': us_gr})


def vacancy(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    vacancy = Vacancy.objects.all()
    return render(request, 'mainapp/vacancy.html', {'vacancy': vacancy, 'us_gr': us_gr})


def products(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'
    products = Product.objects.all()
    return render(request, 'mainapp/products/products.html', {'products': products, 'us_gr': us_gr})


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    # Check if the product is already in the cart for the current user
    cart_product = Cart.objects.filter(user=request.user, products=product).first()

    if cart_product:
        cart_product.quantity += 1
        cart_product.save()
    else:
        Cart.objects.create(user=request.user, products=product)

    return redirect('/cart')


@login_required
def cart(request):
    total = 0
    discount = 0
    try:
        cart = Cart.objects.get(user=request.user)
        if request.method == 'POST':
            promo_code = request.POST.get('promo_code')
            if PromoCode.objects.filter(code=promo_code).exists():
                promo_code = PromoCode.objects.get(code=promo_code)
                discount = promo_code.discount_percentage

            new_quantity = int(request.POST.get('quantity'))
            cart.quantity = new_quantity
            cart.save()
        total = cart.products.price*cart.quantity
        total = total * (100 - discount) / 100
    except:
        return render(request, 'mainapp/products/cart.html', {'user': request.user.username})

    return render(request, 'mainapp/products/cart.html', {'cart': cart,
                                                          'total': total, 'user': request.user.username})


def clear_cart(request, id):
    cart = Cart.objects.get(id=id)
    """
    cart.quantity = 0
    cart.save()
    """
    cart.delete()
    return redirect('/reviews')


def purchase_cart(request, id):
    total = 0
    discount = 0
    try:
        promo_code = request.POST.get('promo_code')
    except:
        promo_code = None

    if PromoCode.objects.filter(code=promo_code).exists():
        promo_code = PromoCode.objects.get(code=promo_code)
        discount = promo_code.discount_percentage

    cart = Cart.objects.get(id=id)
    total = cart.products.price*cart.quantity
    total = total * (100 - discount) / 100

    quantity = cart.quantity
    product = cart.products.name
    customer = Customer.objects.get(user=request.user)
    customer.spendings += total
    customer.save()
    cart.quantity = 0
    #cart.products = None
    cart.save()
    #cart.delete()
    return render(request, 'mainapp/products/purchase_cart.html',
                  {'total': total, 'quantity': quantity, 'product': product, 'pr': promo_code})
