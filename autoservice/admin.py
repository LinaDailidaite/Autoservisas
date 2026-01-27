from .models import Service, Car, Order, OrderLine
from django.contrib import admin


admin.site.register(Service)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(OrderLine)