from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import SiteOwner_receivable

from unfold.admin import ModelAdmin


class SiteOwner_receivableAdmin(ModelAdmin):
    def has_add_permission(self, request):
        # If there's already an instance, don't allow adding another
        if SiteOwner_receivable.objects.exists():
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


admin.site.register(SiteOwner_receivable, SiteOwner_receivableAdmin)
