from django.urls import path
from .views import product_workflow_detail

urlpatterns = [
    path('product_workflow/<int:product_workflow_id>/', product_workflow_detail, name='product_workflow_detail'),
]

