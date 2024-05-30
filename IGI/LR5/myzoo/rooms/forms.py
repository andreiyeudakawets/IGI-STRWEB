from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['image', 'number', 'title', 'pond', 'heating']
