from django.contrib import admin
from .models import *

from unfold.admin import ModelAdmin, TabularInline

# Register your models here.
# admin.site.register(investmenter_dresses)
# admin.site.register(investmenter_balance)


class InvestmenterBalanceInline(TabularInline):
    model = investmenter_balance
    extra = 1  # Number of empty forms to display initially


class InvestmenterDetailsAdmin(ModelAdmin):
    list_display = (
        "user",
        "mobile",
        "account_owner_name",
    )
    inlines = [InvestmenterBalanceInline]


# # Register the admin classes
admin.site.register(investmenter_details, InvestmenterDetailsAdmin)
