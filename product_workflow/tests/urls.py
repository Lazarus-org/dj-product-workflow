from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('product_workflow/', include("product_workflow.urls")),
]
