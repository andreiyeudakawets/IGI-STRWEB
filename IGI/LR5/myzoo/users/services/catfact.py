import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


@login_required
def fact_cat(request):
    us_gr = ''
    if request.user.groups.filter(name='worker').exists():
        us_gr = 'worker'
    elif request.user.groups.filter(name='customer').exists():
        us_gr = 'customer'

    url = 'https://catfact.ninja/facts'
    response = requests.get(url)
    data = response.json()
    facts = data['data']
    return render(request, 'users/facts.html', {'data': facts, 'us_gr': us_gr})
