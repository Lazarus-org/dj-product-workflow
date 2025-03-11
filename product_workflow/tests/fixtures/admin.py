import pytest
from django.contrib.admin import AdminSite
from django.test import RequestFactory

from product_workflow.admin import ProductAdmin, TransitionAdmin
from product_workflow.models import Product, Transition


@pytest.fixture
def request_factory() -> RequestFactory:
    """
    Fixture to provide an instance of RequestFactory.

    Returns:
    -------
        RequestFactory: An instance of Django's RequestFactory.
    """
    return RequestFactory()


@pytest.fixture
def admin_site() -> AdminSite:
    """
    Fixture to provide an instance of AdminSite.

    Returns:
    -------
        AdminSite: An instance of Django's AdminSite.
    """
    return AdminSite()


@pytest.fixture
def product_admin(admin_site: AdminSite) -> ProductAdmin:
    """
    Fixture to provide an instance of ProductAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        ProductAdmin: An instance of ProductAdmin.
    """
    return ProductAdmin(Product, admin_site)


@pytest.fixture
def transition_admin(admin_site: AdminSite):
    """
    Fixture providing an instance of TransitionAdmin.
    """
    return TransitionAdmin(Transition, admin_site)
