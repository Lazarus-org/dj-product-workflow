import sys

import pytest
from django.contrib import admin

from product_workflow.admin import TransitionAdmin
from product_workflow.models import Transition
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestTransitionAdmin:
    """
    Tests for the TransitionAdmin class in the Django admin interface.

    This test class verifies the general functionality of the TransitionAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface without relying on specific field names.

    Tests:
    -------
    - test_admin_registered: Verifies the Transition model is registered with TransitionAdmin.
    - test_list_display_configured: Ensures list_display is defined and non-empty.
    - test_list_view_renders: Tests that the list view renders without errors.
    - test_add_transition: Verifies a transition can be added via the admin.
    """

    def test_admin_registered(self):
        """
        Test that the Transition model is registered with TransitionAdmin in the admin site.

        Asserts:
        --------
            The admin site has Transition registered with an instance of TransitionAdmin.
        """
        assert isinstance(admin.site._registry[Transition], TransitionAdmin)

    def test_list_display_configured(self, transition_admin: TransitionAdmin) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        This ensures the admin list view has some fields configured without
        specifying exact field names.

        Args:
        ----
            transition_admin (TransitionAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(transition_admin.list_display, (tuple, list))
        assert len(transition_admin.list_display) > 0

    def test_add_transition(self, admin_client, product_workflow, step, another_step) -> None:
        """
        Test that a Transition can be added via the admin interface.

        Simulates adding a transition through the admin and verifies it’s created.

        Args:
        ----
            admin_client: Django test client with admin privileges.
            product_workflow: Fixture providing a ProductWorkflow.
            step: Fixture providing an example step.
            another_step: Fixture providing an example step.

        Asserts:
        --------
            A new Transition is created successfully with a 302 redirect.
            The transition count increases by 1.
        """
        product_workflow, step1, step2 = product_workflow, step, another_step

        initial_count = Transition.objects.count()

        response = admin_client.post(
            "/admin/product_workflow/transition/add/",
            {
                "from_step": step1.pk,
                "to_step": step2.pk,
                "condition": "Test condition",
            },
        )

        assert response.status_code == 302  # Redirect after successful save
        assert Transition.objects.count() == initial_count + 1
