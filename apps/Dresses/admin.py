from django.contrib import admin
from .models import *
from .forms import dressImagesForm
# Register your models here.


from unfold.admin import ModelAdmin , StackedInline

admin.site.site_header  = 'emilys luxury Admin Panel'
admin.site.site_title  = 'emilys luxury Admin Panel'

class dressesPhotoInline(StackedInline):  # Or admin.StackedInline for a different layout
    model = dress_images
    form = dressImagesForm
    extra = 1  # Number of empty forms to display

class DressesAdmin(ModelAdmin):
    inlines = [dressesPhotoInline ]
    list_display = ( 'id','designer_name', 'status','price_for_3days' , 'actual_price' ,'is_special' ,
                    'is_approved' ,'product_type', 'is_investment'  )  
    list_filter = ('status','is_approved','is_special','product_type' , 'designer_name',) 
    search_fields = ('id' , )  
    list_editable = ('is_special',)

class N_of_visitors_Admin(ModelAdmin):
    list_display = ('get_dress_id', 'number_of_visitors')
    search_fields = ('dress__id',)  # This is correct for search_fields

    def get_dress_id(self, obj):
        return obj.dress.id
    get_dress_id.admin_order_field = 'dress__id'  # Allows column order sorting
    get_dress_id.short_description = 'Dress ID' 







admin.site.register(dress_busy_days) #Todo delete it __________________________







admin.site.register(Dresses , DressesAdmin)
admin.site.register(dress_number_of_visitors ,N_of_visitors_Admin )


from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import TokenProxy
admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
admin.site.unregister(EmailAddress)