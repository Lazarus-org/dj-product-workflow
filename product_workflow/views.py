from django.views.generic import DetailView, ListView, View

from product_workflow.models import ProductWorkflow, Transition
from product_workflow.settings.conf import config


class BaseProductWorkflowView(config.auth_mixin_class or object, View):
    """A base view for Product Workflow views.

    It dynamically applies authentication based on settings.

    """


class ProductWorkflowListView(BaseProductWorkflowView, ListView):
    """Displays a list of all product workflows."""

    model = ProductWorkflow
    queryset = ProductWorkflow.objects.select_related("product", "workflow").all()
    template_name = "product_workflow_list.html"
    context_object_name = "product_workflows"
    ordering = config.view_ordering_fields


class ProductWorkflowDetailView(BaseProductWorkflowView, DetailView):
    """Displays the details of a specific product workflow, including its steps
    and transitions."""

    model = ProductWorkflow
    queryset = (
        ProductWorkflow.objects.select_related(
            "product", "workflow", "first_step", "last_step"
        )
        .prefetch_related("workflow__steps")
        .all()
    )
    template_name = "product_workflow_detail.html"
    context_object_name = "product_workflow"
    pk_url_kwarg = "product_workflow_id"

    def get_context_data(self, **kwargs):
        """Extends the default context with related steps and transitions."""
        context = super().get_context_data(**kwargs)
        product_workflow = self.object

        context["steps"] = product_workflow.workflow.steps.all().order_by("order")
        context["transitions"] = Transition.objects.select_related(
            "from_step", "to_step"
        ).filter(workflow=product_workflow.workflow)

        return context
