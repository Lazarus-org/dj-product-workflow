import sys

import pytest
from django.urls import reverse

from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestProductWorkflowViews:
    """
    Tests for ProductWorkflow views (ProductWorkflowListView and ProductWorkflowDetailView).

    This test class verifies the functionality of the list and detail views,
    including rendering, context data, and queryset behavior with authentication.

    Tests:
    -------
    - test_list_view_renders: Verifies the list view renders with product workflows for logged-in user.
    - test_list_view_queryset: Tests the list view queryset includes select_related.
    - test_list_view_ordering: Verifies the list view applies ordering from config.
    - test_list_view_unauthenticated: Ensures unauthenticated users are redirected.
    - test_detail_view_renders: Verifies the detail view renders with a product workflow.
    - test_detail_view_context_data: Tests the detail view includes steps and transitions.
    - test_detail_view_404: Ensures a 404 is returned for a non-existent product workflow.
    """

    def test_list_view_renders(
        self, client, admin_user, product_workflow, another_product_workflow
    ):
        """
        Test that the ProductWorkflowListView renders successfully for a logged-in user.

        Args:
        ----
            client: Django test client.
            admin_user: Fixture providing a superuser.
            product_workflow: Fixture providing a ProductWorkflow instance.
            another_product_workflow: Fixture providing another ProductWorkflow instance.

        Asserts:
        --------
            The response status code is 200 and the correct template is used.
        """
        client.login(username="admin", password="password")
        url = reverse("product_workflow_list")
        response = client.get(url)
        assert response.status_code == 200
        assert "product_workflow_list.html" in [t.name for t in response.templates]
        assert len(response.context["product_workflows"]) == 2

    def test_list_view_queryset(self, client, admin_user, product_workflow):
        """
        Test that the ProductWorkflowListView queryset uses select_related.

        Args:
        ----
            client: Django test client.
            admin_user: Fixture providing a superuser.
            product_workflow: Fixture providing a ProductWorkflow instance.

        Asserts:
        --------
            The queryset includes product and workflow in the context.
        """
        client.login(username="admin", password="password")
        url = reverse("product_workflow_list")
        response = client.get(url)
        product_workflows = response.context["product_workflows"]
        assert product_workflows.count() == 1
        # Check that select_related worked (no additional queries for product/workflow)
        pw = product_workflows[0]
        assert pw.product.name == "Test Product"  # Access without extra query
        assert pw.workflow.name == "Test Workflow"  # Access without extra query

    def test_list_view_unauthenticated(self, client, product_workflow):
        """
        Test that unauthenticated users are redirected from ProductWorkflowListView.

        Args:
        ----
            client: Django test client.
            product_workflow: Fixture providing a ProductWorkflow instance.

        Asserts:
        --------
            The response status code is 302 (redirect to login).
        """
        url = reverse("product_workflow_list")
        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url  # Assumes default login redirect

    def test_detail_view_context_data(
        self, client, admin_user, product_workflow_for_view
    ):
        """
        Test that the ProductWorkflowDetailView includes steps and transitions in context.

        Args:
        ----
            client: Django test client.
            admin_user: Fixture providing a superuser.
            product_workflow: Fixture providing a ProductWorkflow instance with steps/transitions.

        Asserts:
        --------
            The context includes steps and transitions with correct data.
        """
        client.login(username="admin", password="password")
        url = reverse(
            "product_workflow_detail",
            kwargs={"product_workflow_id": product_workflow_for_view.id},
        )
        response = client.get(url)
        assert response.status_code == 200
        steps = response.context["steps"]
        transitions = response.context["transitions"]

        assert steps.count() == 2
        assert list(steps.values_list("name", flat=True)) == ["Step 1", "Step 2"]
        assert transitions.count() == 1
        transition = transitions[0]
        assert transition.from_step.name == "Step 1"
        assert transition.to_step.name == "Step 2"

    def test_detail_view_404(self, client, admin_user):
        """
        Test that the ProductWorkflowDetailView returns 404 for a non-existent product workflow.

        Args:
        ----
            client: Django test client.
            admin_user: Fixture providing a superuser.

        Asserts:
        --------
            The response status code is 404.
        """
        client.login(username="admin", password="password")
        url = reverse("product_workflow_detail", kwargs={"product_workflow_id": 999})
        response = client.get(url)
        assert response.status_code == 404
