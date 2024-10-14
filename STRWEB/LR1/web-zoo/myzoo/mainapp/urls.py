from django.urls import path, re_path
from . import views
from tickets.views import list_codes

app_name = 'mainapp'

urlpatterns = [
    #re_path(r'^about/contact', views.contact),
    path('', views.index),
    re_path('about', views.about),
    path('news', views.news, name='news'),
    path('get_news/<int:id>', views.get_news, name='get_news'),
    path('questions', views.questions, name='questions'),
    #path('answers/<int:id>', views.answers, name='answers'),
    path('codes', list_codes, name='codes'),
    path('reviews', views.allreviews, name='reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('delete_review/<int:id>', views.delete_review, name='delete_review'),
    path('privacy', views.privacy, name='privacy'),
    path('vacancy', views.vacancy, name='vacancy'),
    path('products', views.products, name='products'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('clear_cart/<int:id>', views.clear_cart, name='clear_cart'),
    path('purchase_cart/<int:id>', views.purchase_cart, name='purchase_cart'),
    #path('about', views.about),
    #path('contact', views.contact),
]
