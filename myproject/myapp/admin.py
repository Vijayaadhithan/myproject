from django.contrib import admin

# Register your models here.

from .models import User, Trader, Order, Appointment, Review

admin.site.register(User)
admin.site.register(Trader)
admin.site.register(Order)
admin.site.register(Appointment)
admin.site.register(Review)
