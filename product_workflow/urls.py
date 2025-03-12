from django.urls import path

from .views import ProductWorkflowDetailView, ProductWorkflowListView

urlpatterns = [
    path(
        "product_workflow/",
        ProductWorkflowListView.as_view(),
        name="product_workflow_list",
    ),
    path(
        "product_workflow/<int:product_workflow_id>/",
        ProductWorkflowDetailView.as_view(),
        name="product_workflow_detail",
    ),
]
