from datetime import date

from django import forms
from .models import Ticket, Discount, PromoCode


class TicketForm(forms.ModelForm):

    promocode = forms.CharField(
        required=False,  # Делаем поле необязательным
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Промокод'
            }
        )
    )

    class Meta:
        model = Ticket
        fields = ('weekday', )
        widgets = {
            'weekday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def set_ticket_price(self):
        weekday = self.cleaned_data.get('weekday')
        if weekday < date.today():
            self.add_error('rental_date', 'Error.')
        # Calculate the price based on the selected weekday
        if weekday.weekday() in [0, 1, 2, 3, 4]:  # Monday, Tuesday, Wednesday...
            self.instance.price = 10
        else:
            self.instance.price = 15


class DiscountForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Название скидки'
            }
        )
    )
    percentage = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Процент скидки'
            }
        )
    )

    class Meta:
        model = Discount
        fields = ['name', 'percentage']


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code', 'discount_percentage']

class DateForm(forms.Form):
    date = forms.DateField()



