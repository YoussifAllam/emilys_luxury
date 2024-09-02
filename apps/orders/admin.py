from django.contrib import admin
from .models import Order , OrderDetails
from simple_history.admin import SimpleHistoryAdmin

class OrderDetailsInline(admin.StackedInline):
    model = OrderDetails
    extra = 1  # Number of empty forms to display initially

class OrderAdmin(SimpleHistoryAdmin):
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