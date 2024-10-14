import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class AgeService:
    @staticmethod
    def get_age_name(name):
        return requests.get(f'https://api.agify.io/?name={name}').json()


#@login_required
class AgifyView(APIView):
    def get(self, request):

        name = request.GET.get('name')
        if name:
            data = AgeService.get_age_name(name)
            if data:

                return render(request, 'users/age.html', {'name': name, 'data': data})
            else:
                return render(request, 'users/age.html')
        else:
            return render(request, 'users/age.html')

def agify(request):
    name = request.GET.get('name')  # Получаем имя из параметров запроса
    if name:
        url = f'https://api.agify.io/?name={name}'
        response = requests.get(url)
        data = response.json()
        return render(request, 'users/age.html', {'name': name, 'data': data})
    else:
        return render(request, 'users/age.html')
