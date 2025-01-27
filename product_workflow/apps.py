from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ProductWorkflowConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product_workflow"
    verbose_name = _("Django Product Workflow")
