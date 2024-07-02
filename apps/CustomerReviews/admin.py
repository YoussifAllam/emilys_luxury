from django.contrib import admin
from .models import CustomerReviews
# Register your models here.

class   CustomerReviewsAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'Rating_stars' , 'uploaded_at']
    list_filter = ['Rating_stars' ]

admin.site.register(CustomerReviews , CustomerReviewsAdmin)
