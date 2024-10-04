from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin


class paymentAdmin(ModelAdmin):
    list_display = ("id", "order_uuid", "status", "created_at")


admin.site.register(Payment, paymentAdmin)
