import re
from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.forms import DateInput
from employees.models import Customer, Employee


def calculate_age(birth_date: datetime):
    current_date = datetime.now().date()
    age = current_date.year - birth_date.year
    if current_date.month < birth_date.month or (current_date.month == birth_date.month and current_date.day < birth_date.day):
        age -= 1
    return age


class CustomerCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(required=True, widget=DateInput(attrs={'placeholder': 'DD/MM/YYYY'},
                                                                    format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'phone_number', 'date_of_birth']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        user_age = calculate_age(date_of_birth)
        if user_age < 18:
            raise forms.ValidationError('Вам нет 18!')
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        PHONE_NUMBER_REGEX = r"^\+375(\s+)?\(?(17|29|33|44)\)?(\s+)?[0-9]{3}-[0-9]{2}-[0-9]{2}$"
        if not re.match(PHONE_NUMBER_REGEX, phone_number):
            raise forms.ValidationError('Некорректный формат телефонного номера')
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data.get('phone_number')
        date_of_birth = self.cleaned_data.get('date_of_birth')

        if commit:
            user.save()

            group = Group.objects.get(name='customer')
            group.user_set.add(user)

            customer = Customer(user=user, phone_number=phone_number, age=calculate_age(date_of_birth))
            customer.save()

        return user


class CustomerChangeForm(UserChangeForm):
    image = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        PHONE_NUMBER_REGEX = r"^\+375(\s+)?\(?(17|29|33|44)\)?(\s+)?[0-9]{3}-[0-9]{2}-[0-9]{2}$"
        if not re.match(PHONE_NUMBER_REGEX, phone_number):
            raise forms.ValidationError('Некорректный формат телефонного номера')
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        group = Group.objects.get(name='worker')
        if group in user.groups.all():
            employee = user.employee
            employee.image = self.cleaned_data['image']
            employee.phone_number = self.cleaned_data['phone_number']
            employee.save()
        group = Group.objects.get(name='customer')
        if group in user.groups.all():
            customer = user.customer
            customer.image = self.cleaned_data['image']
            customer.phone_number = self.cleaned_data['phone_number']
            customer.save()
        return user




