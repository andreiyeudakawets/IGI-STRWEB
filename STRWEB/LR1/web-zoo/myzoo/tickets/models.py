from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_percentage = models.PositiveIntegerField()

    def __str__(self):
        return self.code


class Ticket(models.Model):
    price = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.DateField(default=timezone.now().date())
    promocode = models.ForeignKey(PromoCode, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Билет {self.id} пользовтеля {self.user.username}'


        return f'Корзина {self.user.username}'
"""
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tickets = models.ManyToManyField('Ticket', through='CartItem')


class CartItem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):

"""






