from django.contrib import admin
from .models import *

# from tinymce.widgets import TinyMCE
# Register your models here.

from unfold.admin import ModelAdmin, StackedInline


class FAQAdmin(ModelAdmin):
    list_display = ("question", "answer", "Which_Page")
    list_filter = ("Which_Page",)
    # formfield_overrides = {
    #     HTMLField: {'widget': TinyMCE()},
    # }


admin.site.register(FAQ, FAQAdmin)


class TermsAdmin(ModelAdmin):
    list_display = ("title", "Which_Page", "description", "index", "language")
    list_filter = ("Which_Page",)
    list_editable = ("index", "language")
    # formfield_overrides = {
    #     HTMLField: {'widget': TinyMCE()},
    # }


admin.site.register(terms_and_condations, TermsAdmin)
