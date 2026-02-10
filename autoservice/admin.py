from .models import Service, Car, Order, OrderLine, OrderReview, CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class ServiceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'price']

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ['line_sum']
    extra = 1
    autocomplete_fields = ['service']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'due_back', 'is_on_time', 'reader', 'total']
    inlines = [OrderLineInline]

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity', 'line_sum']

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'client_name', 'license_plate', 'vin_code']
    list_filter = ['make', 'model', 'client_name']
    search_fields = ['license_plate', 'vin_code']

class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'date_created', 'reviewer', 'content']

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("photo", )}),
    )

admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(CustomUser, CustomUserAdmin)