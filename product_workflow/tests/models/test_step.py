import sys

import pytest
from django.core.exceptions import ValidationError

from product_workflow.models import Step
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestStep:
    """
    Tests for the Step model.

    This test class verifies the general functionality of the Step model,
    including its string representation and validation logic in the clean method.

    Tests:
    -------
    - test_str_representation: Verifies the __str__ method returns the expected format.
    - test_clean_valid_instance: Tests that clean passes with a valid instance.
    - test_clean_duplicate_name: Tests that clean raises ValidationError for duplicate name.
    - test_clean_duplicate_order: Tests that clean raises ValidationError for duplicate order.
    - test_unique_name_constraint: Verifies the database-level unique constraint on name.
    - test_unique_order_constraint: Verifies the database-level unique constraint on order.
    """

    def test_str_representation(self, step):
        """
        Test the __str__ method.

        Verifies that the string representation includes name and order in the expected format.

        Args:
        ----
            step: Fixture providing a Step instance.

        Asserts:
        --------
            The __str__ output matches the expected format.
        """
        expected_str = f"{step.name} (Order: {step.order})"
        assert str(step) == expected_str

    def test_clean_valid_instance(self, workflow):
        """
        Test that the clean method passes for a valid Step instance.

        Creates a new Step and ensures no ValidationError is raised.

        Args:
        ----
            workflow: Fixture providing a Workflow instance.
        """
        step = Step(workflow=workflow, name="Unique Step", order=3)
        try:
            step.clean()
        except ValidationError:
            pytest.fail("clean() raised ValidationError unexpectedly")

    def test_clean_duplicate_name(self, step, workflow):
        """
        Test that the clean method raises ValidationError for a duplicate name.

        Attempts to create a second Step with the same name in the same workflow,
        verifying that clean enforces the uniqueness constraint.

        Args:
        ----
            step: Fixture providing an existing Step instance.
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            A ValidationError is raised with the expected message.
        """
        duplicate_step = Step(
            workflow=workflow,
            name=step.name,  # Same name as existing step
            order=3,  # Different order
        )
        with pytest.raises(ValidationError) as exc_info:
            duplicate_step.clean()
        assert "An step with this name already exists" in str(exc_info.value)

    def test_clean_duplicate_order(self, step, workflow):
        """
        Test that the clean method raises ValidationError for a duplicate order.

        Attempts to create a second Step with the same order in the same workflow,
        verifying that clean enforces the uniqueness constraint.

        Args:
        ----
            step: Fixture providing an existing Step instance.
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            A ValidationError is raised with the expected message.
        """
        duplicate_step = Step(
            workflow=workflow,
            name="Different Name",
            order=step.order,  # Same order as existing step
        )
        with pytest.raises(ValidationError) as exc_info:
            duplicate_step.clean()
        assert "An step with this execution order already exists" in str(exc_info.value)

    def test_unique_name_constraint(self, step, workflow):
        """
        Test the database-level unique constraint on (workflow, name).

        Attempts to create a duplicate Step with the same name in the database and verifies
        that an IntegrityError (or similar) is raised.

        Args:
        ----
            step: Fixture providing an existing Step instance.
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            Creating a duplicate raises an exception.
        """
        with pytest.raises(Exception) as exc_info:  # IntegrityError or similar
            Step.objects.create(
                workflow=workflow,
                name=step.name,  # Same name
                order=3,  # Different order
            )
        assert (
            "UNIQUE constraint failed:" in str(exc_info.value)
            or "duplicate" in str(exc_info.value).lower()
        )

    def test_unique_order_constraint(self, step, workflow):
        """
        Test the database-level unique constraint on (workflow, order).

        Attempts to create a duplicate Step with the same order in the database and verifies
        that an IntegrityError (or similar) is raised.

        Args:
        ----
            step: Fixture providing an existing Step instance.
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            Creating a duplicate raises an exception.
        """
        with pytest.raises(Exception) as exc_info:  # IntegrityError or similar
            Step.objects.create(
                workflow=workflow,
                name="Different Name",
                order=step.order,  # Same order
            )
        assert (
            "UNIQUE constraint failed:" in str(exc_info.value)
            or "duplicate" in str(exc_info.value).lower()
        )
