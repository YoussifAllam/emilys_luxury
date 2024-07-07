from django.contrib import admin
from .models import Coupon
# Register your models here.

class couponsAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_to', 'discount')
    list_filter = ('valid_to',) 
    search_fields = ('valid_to' , 'code' ) 

admin.site.register(Coupon , couponsAdmin)
