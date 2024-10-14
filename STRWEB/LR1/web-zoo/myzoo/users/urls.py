from django.urls import path, re_path
from . import views
from .views import CustomerUpdateView
from .services.agebyname import AgifyView, agify
from .services.catfact import fact_cat

app_name = 'users'

urlpatterns = [
    re_path(r'^register/', views.register),
    re_path(r'^login/', views.user_login, name='login'),
    #path('logout/', views.user_logout, name='logout'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:pk>/', CustomerUpdateView.as_view(), name='user_update'),
    path('delete-customer/<int:customer_id>/', views.delete_user, name='delete_customer'),
    path('profile/', views.user_profile, name='profile'),
    #re_path(r'^profile/', views.user_profile),
    path('customers/', views.customers_list, name='customers'),
    #re_path(r'^customers/', views.customers_list, name='customers'),
    path('agify/', agify, name='agify'),
    #re_path(r'^agify/', AgifyView.as_view(), name='agify'),
    path('fact/', fact_cat, name='cat_facts'),
    #path('users-cart/', views.users_cart),
]
