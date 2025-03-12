from django.contrib import admin

from product_workflow.models import Step
from product_workflow.settings.conf import config


@admin.register(Step, site=config.admin_site_class)
class StepAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "order",
        "workflow",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name")
    search_fields = ("name", "description", "workflow__name")
    list_filter = ("workflow", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("workflow", "order")
    autocomplete_fields = ("workflow",)
