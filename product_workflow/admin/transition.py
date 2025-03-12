from django.contrib import admin

from product_workflow.models import Transition
from product_workflow.settings.conf import config


@admin.register(Transition, site=config.admin_site_class)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ("id", "from_step", "to_step", "condition", "workflow")
    list_display_links = ("id", "from_step")
    search_fields = ("workflow__name", "from_step__name", "to_step__name")
    list_filter = ("workflow",)
    ordering = ("workflow", "from_step", "to_step")
    autocomplete_fields = ("from_step", "to_step")
    readonly_fields = ("workflow",)
