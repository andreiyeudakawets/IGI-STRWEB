from django.contrib import admin

from .models import Ticket, PromoCode, Discount

admin.site.register(Discount)
admin.site.register(PromoCode)
admin.site.register(Ticket)
"""
admin.site.register(CartItem)"""
