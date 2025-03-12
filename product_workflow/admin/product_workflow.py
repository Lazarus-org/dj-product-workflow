from django.contrib import admin

from product_workflow.models import ProductWorkflow
from product_workflow.settings.conf import config


@admin.register(ProductWorkflow, site=config.admin_site_class)
class ProductWorkflowAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "workflow",
        "first_step",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "product")
    search_fields = (
        "product__name",
        "workflow__name",
        "first_step__name",
        "last_step__name",
    )
    list_filter = ("workflow", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("product", "workflow")
    autocomplete_fields = ("product", "workflow", "first_step", "last_step")
