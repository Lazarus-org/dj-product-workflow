import sys

import pytest
from django.core.exceptions import ValidationError

from product_workflow.models import Transition
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestTransition:
    """
    Tests for the Transition model.

    This test class verifies the general functionality of the Transition model,
    including its string representation and validation logic in the clean method.

    Tests:
    -------
    - test_str_representation: Verifies the __str__ method returns the expected format.
    - test_str_with_missing_steps: Tests __str__ when steps are missing.
    - test_clean_valid_instance: Tests that clean passes with a valid instance.
    - test_clean_auto_sets_product_workflow: Tests that clean sets product_workflow automatically.
    - test_clean_missing_steps: Tests that clean raises ValidationError for missing steps.
    - test_clean_mismatched_workflows: Tests that clean raises ValidationError for mismatched workflows.
    - test_clean_duplicate_transition: Tests that clean raises ValidationError for duplicates.
    - test_unique_constraint: Verifies the database-level unique constraint.
    """

    def test_str_representation(self, transition, step, another_step, workflow):
        """
        Test the __str__ method with valid steps.

        Verifies that the string representation includes from_step.name, to_step.name,
        and product_workflow_id in the expected format.

        Args:
        ----
            transition: Fixture providing a Transition instance.
            step: Fixture providing a From Step instance.
            another_step: Fixture providing a To Step instance.
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            The __str__ output matches the expected format.
        """
        expected_str = (
            f"{step.name} -> {another_step.name} (Workflow ID: {workflow.id})"
        )
        assert str(transition) == expected_str

    def test_str_with_missing_steps(self, workflow):
        """
        Test the __str__ method when steps are missing.

        Verifies that __str__ defaults to "Unknown" for missing from_step or to_step.

        Args:
        ----
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            The __str__ output includes "Unknown" for missing steps.
        """
        transition = Transition(workflow=workflow)  # No steps set
        expected_str = f"Unknown -> Unknown (Workflow ID: {workflow.id})"
        assert str(transition) == expected_str

    def test_clean_valid_instance(self, step, another_step):
        """
        Test that the clean method passes for a valid Transition instance.

        Creates a new Transition and ensures no ValidationError is raised.

        Args:
        ----
            step: Fixture providing a From Step instance.
            another_step: Fixture providing a To Step instance.
        """
        transition = Transition(
            from_step=step, to_step=another_step
        )  # product_workflow auto-set
        try:
            transition.clean()
        except ValidationError:
            pytest.fail("clean() raised ValidationError unexpectedly")

    def test_clean_auto_sets_product_workflow(self, step, another_step):
        """
        Test that the clean method automatically sets workflow from from_step.

        Creates a Transition without product_workflow and verifies it’s set correctly.

        Args:
        ----
            step: Fixture providing a From Step instance.
            another_step: Fixture providing a To Step instance.

        Asserts:
        --------
            workflow is set to from_step.workflow.
        """
        transition = Transition(
            from_step=step, to_step=another_step
        )  # No product_workflow initially
        transition.clean()
        assert transition.workflow == step.workflow

    def test_clean_missing_steps(self, workflow):
        """
        Test that the clean method raises ValidationError when steps are missing.

        Creates a Transition with missing from_step or to_step and verifies the error.

        Args:
        ----
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            A ValidationError is raised with the expected message.
        """
        transition = Transition(workflow=workflow, to_step=None)  # Missing from_step
        with pytest.raises(ValidationError) as exc_info:
            transition.clean()
        assert "Both 'From Step' and 'To Step' must be specified" in str(exc_info.value)

    def test_clean_same_steps(self, workflow, step):
        """
        Test that the clean method raises ValidationError when steps are the same.

        Creates a Transition with one step as from_step and to_step and verifies the error.

        Args:
        ----
            workflow: Fixture providing a Workflow instance.
            step: Fixture providing a From Step instance.

        Asserts:
        --------
            A ValidationError is raised with the expected message.
        """
        transition = Transition(workflow=workflow, from_step=step, to_step=step)
        with pytest.raises(ValidationError) as exc_info:
            transition.clean()
        assert "The from step and to step cannot be the same." in str(exc_info.value)

    def test_clean_mismatched_workflows(self, step, step_from_different_workflow):
        """
        Test that the clean method raises ValidationError for mismatched workflows.

        Creates a Transition with steps from different product_workflows and verifies the error.

        Args:
        ----
            step: Fixture providing a From Step instance.
            step_from_different_workflow: Fixture providing a Step from a different workflow.

        Asserts:
        --------
            A ValidationError is raised with the expected message.
        """
        transition = Transition(from_step=step, to_step=step_from_different_workflow)
        with pytest.raises(ValidationError) as exc_info:
            transition.clean()
        assert "'From Step' and 'To Step' must belong to the same workflow" in str(
            exc_info.value
        )

    def test_clean_duplicate_transition(self, transition, step, another_step, workflow):
        """
        Test that the clean method raises ValidationError for a duplicate transition.

        Attempts to create a second Transition with the same workflow, from_step, and to_step.

        Args:
        ----
            transition: Fixture providing an existing Transition instance.
            step: Fixture providing a From Step instance.
            another_step: Fixture providing a To Step instance.
            workflow: Fixture providing a ProductWorkflow instance.

        Asserts:
        --------
            A ValidationError is raised with the expected message.
        """
        duplicate_transition = Transition(
            workflow=workflow,
            from_step=step,
            to_step=another_step,
            condition="Different condition",
        )
        with pytest.raises(ValidationError) as exc_info:
            duplicate_transition.clean()
        assert "A transition between these steps already exists" in str(exc_info.value)

    def test_unique_constraint(self, transition, step, another_step, workflow):
        """
        Test the database-level unique constraint on (workflow, from_step, to_step).

        Attempts to create a duplicate Transition in the database and verifies an exception is raised.

        Args:
        ----
            transition: Fixture providing an existing Transition instance.
            step: Fixture providing a From Step instance.
            another_step: Fixture providing a To Step instance.
            workflow: Fixture providing a Workflow instance.

        Asserts:
        --------
            Creating a duplicate raises an exception.
        """
        with pytest.raises(Exception) as exc_info:  # IntegrityError or similar
            Transition.objects.create(
                workflow=workflow,
                from_step=step,
                to_step=another_step,
                condition="Another condition",
            )
        assert (
            "UNIQUE constraint failed:" in str(exc_info.value)
            or "duplicate" in str(exc_info.value).lower()
        )
