from django.forms import ModelForm
from .models import Animal


class AnimalForm(ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'gender', 'age', 'country', 'amount_of_feed', 'animal_class', 'responsible_employee', 'image']
