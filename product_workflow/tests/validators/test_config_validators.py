import sys
from unittest.mock import patch

import pytest

from product_workflow.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from product_workflow.validators.config_validators import (
    validate_list_fields,
    validate_optional_path_setting,
    validate_optional_paths_setting,
)

pytestmark = [
    pytest.mark.validators,
    pytest.mark.config_validators,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestValidateListFields:
    def test_valid_list(self) -> None:
        """
        Test that a valid list of fields returns no errors.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_list_fields(["field1", "field2"], "SOME_LIST_SETTING")
        assert not errors  # No errors should be returned

    def test_invalid_list_type(self) -> None:
        """
        Test that a non-list setting returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_list_fields("not_a_list", "SOME_LIST_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "product_workflow.E002_SOME_LIST_SETTING"

    def test_empty_list(self) -> None:
        """
        Test that an empty list returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_list_fields([], "SOME_LIST_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "product_workflow.E003_SOME_LIST_SETTING"

    def test_invalid_element_in_list(self) -> None:
        """
        Test that a list containing a non-string element returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_list_fields([123, "valid_field"], "SOME_LIST_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "product_workflow.E004_SOME_LIST_SETTING"


class TestValidateOptionalClassSetting:
    def test_valid_class_import(self) -> None:
        """
        Test that a valid class path returns no errors.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        with patch("django.utils.module_loading.import_string"):
            errors = validate_optional_path_setting(
                "django.contrib.auth.mixins.LoginRequiredMixin",
                "SOME_CLASS_SETTING",
            )
            assert not errors

    def test_invalid_class_import(self) -> None:
        """
        Test that an invalid class path returns an import error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid class paths.
        """
        with patch(
            "django.utils.module_loading.import_string", side_effect=ImportError
        ):
            errors = validate_optional_path_setting(
                "invalid.path.ClassName", "SOME_CLASS_SETTING"
            )
            assert len(errors) == 1
            assert errors[0].id == "product_workflow.E010_SOME_CLASS_SETTING"

    def test_invalid_class_path_type(self) -> None:
        """
        Test that a non-string class path returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for non-string class paths.
        """
        errors = validate_optional_path_setting(12345, "SOME_CLASS_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "product_workflow.E009_SOME_CLASS_SETTING"

    def test_none_class_path(self) -> None:
        """
        Test that a None class path returns no error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_optional_path_setting(None, "SOME_CLASS_SETTING")  # type: ignore
        assert not errors

    def test_none_class_paths(self) -> None:
        """
        Test that a None class paths returns no error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_optional_paths_setting(None, "SOME_CLASS_SETTING")  # type: ignore
        assert not errors

    def test_invalid_list_args_classes_import(self) -> None:
        """
        Test that a list of invalid classes args returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain errors for each invalid class path with the expected error ID.
        """
        errors = validate_optional_paths_setting([1, 5], "SOME_CLASS_SETTING")
        assert len(errors) == 2
        assert errors[0].id == "product_workflow.E012_SOME_CLASS_SETTING"

    def test_invalid_path_classes_import(self) -> None:
        """
        Test that a list of invalid classes path returns an import error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid class paths.
        """
        with patch(
            "django.utils.module_loading.import_string", side_effect=ImportError
        ):
            errors = validate_optional_paths_setting(
                ["INVALID_PATH"], "SOME_CLASS_SETTING"
            )
            assert len(errors) == 1
            assert errors[0].id == "product_workflow.E013_SOME_CLASS_SETTING"

    def test_invalid_type_classes_import(self) -> None:
        """
        Test that a list of invalid classes type returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid class types.
        """
        with patch(
            "django.utils.module_loading.import_string", side_effect=ImportError
        ):
            errors = validate_optional_paths_setting(
                "INVALID_TYPE", "SOME_CLASS_SETTING"
            )
            assert len(errors) == 1
            assert errors[0].id == "product_workflow.E011_SOME_CLASS_SETTING"
