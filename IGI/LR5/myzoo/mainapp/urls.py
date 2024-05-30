from django.urls import path, re_path
from . import views
from tickets.views import list_codes

app_name = 'mainapp'

urlpatterns = [
    #re_path(r'^about/contact', views.contact),
    path('', views.index),
    re_path(r'^about', views.about),
    re_path(r'^news', views.news, name='news'),
    re_path(r'^codes', list_codes, name='codes'),
    re_path(r'^reviews', views.allreviews, name='reviews'),
    re_path(r'^add_review', views.add_review, name='add_review'),
    path(r'^delete_review/<int:id>', views.delete_review, name='delete_review'),
    re_path(r'^privacy_policy', views.privacy),
    #path('about', views.about),
    #path('contact', views.contact),
]
