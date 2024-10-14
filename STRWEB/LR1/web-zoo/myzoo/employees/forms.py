import re

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm

from .models import Employee, EmployeePosition
from rooms.models import Room


class EmployeePositionForm(ModelForm):
    class Meta:
        model = EmployeePosition
        fields = ('title',)


class EmployeeCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=50, required=False)
    age = forms.IntegerField(required=True)
    image = forms.ImageField(required=False)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False)
    position = forms.ModelChoiceField(queryset=EmployeePosition.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'phone_number', 'age', 'image', 'room', 'position']

    def save(self, commit=True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data.get('phone_number')
        age = self.cleaned_data.get('age')
        image = self.cleaned_data.get('image')
        room = self.cleaned_data.get('room')
        position = self.cleaned_data.get('position')

        if commit:
            user.save()

            group = Group.objects.get(name='worker')
            group.user_set.add(user)

            employee = Employee(user=user, phone_number=phone_number, age=age, image=image, room=room,
                                position=position)
            employee.save()

        return user



class EmployeeChangeForm(UserChangeForm):

    image = forms.ImageField(required=False)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False)
    position = forms.ModelChoiceField(queryset=EmployeePosition.objects.all(), required=False)
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
            employee.room = self.cleaned_data['room']
            employee.position= self.cleaned_data['position']
            employee.phone_number = self.cleaned_data['phone_number']
            employee.save()

        return user
