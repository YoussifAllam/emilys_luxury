from django.contrib import admin
from .models import *
# Register your models here.

class FAQAdmin(admin.ModelAdmin):
    list_display = ( 'question' , 'answer' , 'Which_Page')
    list_filter = ('Which_Page',)

admin.site.register(FAQ , FAQAdmin)


class TermsAdmin(admin.ModelAdmin):
    list_display = ( 'title' ,'Which_Page' , 'description')
    list_filter = ('Which_Page',)
admin.site.register(terms_and_condations , TermsAdmin)