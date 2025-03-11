import sys
from unittest.mock import MagicMock, patch

import pytest

from product_workflow.settings.checks import check_product_workflow_settings
from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.settings,
    pytest.mark.settings_checks,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestCheckProductWorkflowSettings:
    @patch("product_workflow.settings.checks.config")
    def test_valid_settings(self, mock_config: MagicMock) -> None:
        """
        Test that valid settings produce no errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with valid settings.

        Asserts:
        -------
            No errors are returned when all settings are valid.
        """
        # Mock the config values to be valid
        mock_config.view_ordering_fields = ["created_at"]
        mock_config.get_setting.side_effect = lambda name, default: None

        errors = check_product_workflow_settings(None)

        # There should be no errors for valid settings
        assert not errors

    @patch("product_workflow.settings.checks.config")
    def test_invalid_list_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid list settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid list settings.

        Asserts:
        -------
            Three errors are returned for invalid list values in settings.
        """
        # Mock the config values with invalid list settings
        mock_config.view_ordering_fields = [123]  # Invalid list element
        mock_config.get_setting.side_effect = lambda name, default: None

        errors = check_product_workflow_settings(None)

        # Expect 1 error for invalid list settings
        assert len(errors) == 1
        assert (
            errors[0].id
            == f"product_workflow.E004_{mock_config.prefix}VIEW_ORDERING_FIELDS"
        )

    @patch("product_workflow.settings.checks.config")
    def test_invalid_path_import(self, mock_config: MagicMock) -> None:
        """
        Test that invalid path import settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid paths.

        Asserts:
        -------
            Seven errors are returned for invalid path imports.
        """
        # Mock the config values with invalid paths
        mock_config.view_ordering_fields = ["created_at"]
        mock_config.get_setting.side_effect = (
            lambda name, default: "invalid.path.ClassName"
        )

        errors = check_product_workflow_settings(None)

        # Expect 2 errors for invalid path imports
        assert len(errors) == 2

        assert (
            errors[0].id
            == f"product_workflow.E010_{mock_config.prefix}ADMIN_SITE_CLASS"
        )
        assert (
            errors[1].id == f"product_workflow.E010_{mock_config.prefix}VIEW_AUTH_MIXIN"
        )
