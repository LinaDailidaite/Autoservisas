from .models import Service, Car, Order, OrderLine
from django.contrib import admin

class ServiceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'price']

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ['line_sum']
    extra = 1
    autocomplete_fields = ['service']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'total']
    inlines = [OrderLineInline]

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity', 'line_sum']

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'client_name', 'license_plate', 'vin_code']
    list_filter = ['make', 'model', 'client_name']
    search_fields = ['license_plate', 'vin_code']


admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)