from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductWorkflowConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product_workflow"
    verbose_name = _("Django Product Workflow")

    def ready(self):
        """This method is called when the application is fully loaded.

        Its main purpose is to perform startup tasks, such as importing
        and registering system checks for validating the configuration
        settings of the app. It ensures that all necessary configurations
        are in place and properly validated when the Django project initializes.

        In this case, it imports the settings checks from the
        `product_workflow.settings` module to validate the configuration
        settings.

        """
        from product_workflow.settings import checks
