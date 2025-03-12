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
    search_fields = ("product__name", "workflow__name", "first_step__name")
    list_filter = ("workflow", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("product", "workflow")
    autocomplete_fields = ("product", "workflow", "first_step")
