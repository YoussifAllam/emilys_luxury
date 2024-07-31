from django.contrib import admin
from .models import invitation_points_Trade , user_invitation_points
# Register your models here.
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages

class invitation_points_Trade_admin(admin.ModelAdmin):
    def has_add_permission(self, request):
            # If there's already an instance, don't allow adding another
            if invitation_points_Trade.objects.exists():
                return False
            return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the instance
        return False

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except ValidationError as e:
            self.message_user(request, e.message, level=messages.ERROR)

admin.site.register(invitation_points_Trade , invitation_points_Trade_admin)
admin.site.register(user_invitation_points)