from django.db import models
from django.utils.translation import gettext_lazy as _

from product_workflow.mixins.models.timestamp import TimeStampModel


class Product(TimeStampModel):
    """Represents a product in the system.

    Attributes:
        name (str): Unique name identifier for the product
        description (str): Detailed information about the product features and specifications
        created_at (datetime): Auto-generated creation timestamp
        updated_at (datetime): Auto-generated last modification timestamp

    """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Product Name"),
        help_text=_("The unique name identifier for the product."),
        db_comment="Stores the unique name of the product (max 255 characters).",
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Detailed information about product features and specifications."),
        db_comment="Contains detailed textual description of the product.",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
