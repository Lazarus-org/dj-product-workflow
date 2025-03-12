from django.contrib import admin

from product_workflow.models import Product
from product_workflow.settings.conf import config


@admin.register(Product, site=config.admin_site_class)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")
    list_display_links = ("id", "name")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("name",)
