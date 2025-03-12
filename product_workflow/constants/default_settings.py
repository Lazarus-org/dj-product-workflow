from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class DefaultAdminSettings:
    admin_site_class: Optional[str] = None


@dataclass(frozen=True)
class DefaultViewSettings:
    view_auth_class: str = "django.contrib.auth.mixins.LoginRequiredMixin"
    view_ordering_fields: List[str] = field(
        default_factory=lambda: ["product__name", "-created_at"]
    )


admin_settings = DefaultAdminSettings()
view_settings = DefaultViewSettings()
