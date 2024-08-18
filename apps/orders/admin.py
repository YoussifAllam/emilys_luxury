from django.contrib import admin
from .models import Order , OrderDetails


class OrderDetailsInline(admin.StackedInline):
    model = OrderDetails
    extra = 1  # Number of empty forms to display initially

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'user','created_at' ,
        'status','is_payment_completed' ,'total_price' ,
        'arrival_date'
    )

    list_filter = (
        'status',
        'is_payment_completed',
    )

    inlines = [OrderDetailsInline]


admin.site.register(Order , OrderAdmin)