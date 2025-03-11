import sys

import pytest
from django.contrib import admin

from product_workflow.admin import ProductAdmin
from product_workflow.models import Product
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestProductAdmin:
    """
    Tests for the ProductAdmin class in the Django admin interface.

    This test class verifies the general functionality of the ProductAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface without relying on specific field names.

    Tests:
    -------
    - test_admin_registered: Verifies the Product model is registered with ProductAdmin.
    - test_list_display_configured: Ensures list_display is defined and non-empty.
    - test_list_view_renders: Tests that the list view renders without errors.
    - test_add_product: Verifies a product can be added via the admin.
    """

    def test_admin_registered(self):
        """
        Test that the Product model is registered with ProductAdmin in the admin site.

        Asserts:
        --------
            The admin site has Product registered with an instance of ProductAdmin.
        """
        assert isinstance(admin.site._registry[Product], ProductAdmin)

    def test_list_display_configured(self, product_admin: ProductAdmin) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        This ensures the admin list view has some fields configured without
        specifying exact field names.

        Args:
        ----
            product_admin (ProductAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(product_admin.list_display, (tuple, list))
        assert len(product_admin.list_display) > 0

    def test_add_product(self, admin_client) -> None:
        """
        Test that a Product can be added via the admin interface.

        Simulates adding a product through the admin and verifies it’s created.

        Args:
        ----
            admin_client: Django test client with admin privileges.

        Asserts:
        --------
            A new Product is created successfully with a 302 redirect.
            The product count increases by 1.
        """
        initial_count = Product.objects.count()

        response = admin_client.post(
            "/admin/product_workflow/product/add/",
            {
                "name": "New Product",
                "description": "New Product Description",
            },
        )

        assert response.status_code == 302  # Redirect after successful save
        assert Product.objects.count() == initial_count + 1
