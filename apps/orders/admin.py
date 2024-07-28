from django.contrib import admin
from .models import Order, OrderItem , order_dress_booking_days

admin.site.register(Order)
admin.site.register(OrderItem)

class booking_days(admin.ModelAdmin):
    list_display = ['day' , 'OrderItem' , 'dress']
admin.site.register(order_dress_booking_days , booking_days)