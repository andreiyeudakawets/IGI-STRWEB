from django.urls import path, re_path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='all_rooms'),
    path('add-room', views.add_room, name='add_room'),
    path('add', views.add_room, name='add_room'),
    path('delete/<int:id>/', views.delete_room, name='delete_room'),
    path('edit/<int:id>/', views.edit_room, name='edit_room'),
]
