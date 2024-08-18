from django.contrib import admin
from .models import User 

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'is_staff' , 'is_approvid' ,
        'user_type' , 'last_login' ,'email_verified'
    )

    list_filter = ('is_staff', 'is_active', 'groups','email_verified')

    search_fields = ('username', 'email')

    ordering = ('username',)
    
admin.site.register(User, UserAdmin)
    