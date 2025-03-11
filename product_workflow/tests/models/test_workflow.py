import sys

import pytest

from product_workflow.models import Workflow
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestWorkflowModel:
    """
    Test suite for the Workflow model.
    """

    def test_str_method(self, workflow: Workflow) -> None:
        """
        Test that the __str__ method returns the correct string representation of a Workflow.

        Asserts:
        -------
            - The string representation of the Workflow includes the name.
        """
        expected_str = workflow.name
        assert (
            str(workflow) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(workflow)}'."
