from django.contrib import admin
from .models import *

class paymentAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'order_uuid' , 'status' ,'created_at')

admin.site.register(Payment , paymentAdmin)
