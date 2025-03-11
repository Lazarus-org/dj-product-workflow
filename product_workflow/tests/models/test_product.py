import sys

import pytest

from product_workflow.models import Product
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestProductModel:
    """
    Test suite for the Product model.
    """

    def test_str_method(self, product: Product) -> None:
        """
        Test that the __str__ method returns the correct string representation of a product.

        Asserts:
        -------
            - The string representation of the product includes the name.
        """
        expected_str = product.name
        assert (
            str(product) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(product)}'."
