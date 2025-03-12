from typing import Any, List

from django.conf import settings
from django.utils.module_loading import import_string

from product_workflow.constants.default_settings import admin_settings, view_settings
from product_workflow.constants.types import DefaultPath, OptionalPaths


class ProductWorkflowConfig:
    """A configuration handler.

    allowing dynamic settings loading from the Django settings, with
    default fallbacks.

    """

    prefix = "PRODUCT_WORKFLOW_"

    def __init__(self) -> None:
        self.admin_site_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}ADMIN_SITE_CLASS",
            admin_settings.admin_site_class,
        )
        self.auth_mixin_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}VIEW_AUTH_MIXIN",
            view_settings.view_auth_class,
        )
        self.view_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}VIEW_ORDERING_FIELDS",
            view_settings.view_ordering_fields,
        )

    def get_setting(self, setting_name: str, default_value: Any) -> Any:
        """Retrieve a setting from Django settings with a default fallback.

        Args:
            setting_name (str): The name of the setting to retrieve.
            default_value (Any): The default value to return if the setting is not found.

        Returns:
            Any: The value of the setting or the default value if not found.

        """
        return getattr(settings, setting_name, default_value)

    def get_optional_paths(
        self,
        setting_name: str,
        default_path: DefaultPath,
    ) -> OptionalPaths:
        """Dynamically load a method or class path on a setting, or return None
        if the setting is None or invalid.

        Args:
            setting_name (str): The name of the setting for the method or class path.
            default_path (Optional[Union[str, List[str]]): The default import path for the method or class.

        Returns:
            Optional[Union[Type[Any], List[Type[Any]]]]: The imported method or class or None
             if import fails or the path is invalid.

        """
        _path: DefaultPath = self.get_setting(setting_name, default_path)

        if _path and isinstance(_path, str):
            try:
                return import_string(_path)
            except ImportError:
                return None
        elif _path and isinstance(_path, list):
            try:
                return [import_string(path) for path in _path if isinstance(path, str)]
            except ImportError:
                return []

        return None


config: ProductWorkflowConfig = ProductWorkflowConfig()
