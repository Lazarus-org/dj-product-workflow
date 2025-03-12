from typing import Any, List

from django.core.checks import Error, register

from product_workflow.settings.conf import config
from product_workflow.validators.config_validators import (
    validate_list_fields,
    validate_optional_path_setting,
)


@register()
def check_product_workflow_settings(app_configs: Any, **kwargs: Any) -> List[Error]:
    """Check and validate product workflow settings in the Django
    configuration.

    This function performs validation of various product workflow-related settings
    defined in the Django settings. It returns a list of errors if any issues are found.

    Parameters:
    -----------
    app_configs : Any
        Passed by Django during checks (not used here).

    kwargs : Any
        Additional keyword arguments for flexibility.

    Returns:
    --------
    List[Error]
        A list of `Error` objects for any detected configuration issues.

    """
    errors: List[Error] = []

    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}ADMIN_SITE_CLASS", None),
            f"{config.prefix}ADMIN_SITE_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}VIEW_AUTH_MIXIN", None),
            f"{config.prefix}VIEW_AUTH_MIXIN",
        )
    )
    errors.extend(
        validate_list_fields(
            config.view_ordering_fields, f"{config.prefix}VIEW_ORDERING_FIELDS"
        )
    )

    return errors
