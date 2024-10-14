from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list),
    path('buy-ticket/', views.buy_ticket),
    path('user-tickets/', views.user_tickets),
    path('add-promo/', views.add_code, name='add_promo'),
    path('all-codes/', views.list_codes, name='codes'),
    path('delete-code/<int:code_id>', views.delete_code, name='del_code'),
    path('edit-code/<int:code_id>', views.edit_code, name='edit_code'),

]
