from django.db import models
from django.utils.translation import gettext_lazy as _

from product_workflow.mixins.models.timestamp import TimeStampModel


class Workflow(TimeStampModel):
    """Represents a workflow process consisting of multiple steps.

    Attributes:
        name (str): Unique name identifier for the workflow
        description (str): Detailed explanation of the workflow's purpose and process
        created_at (datetime): Auto-generated creation timestamp
        updated_at (datetime): Auto-generated last modification timestamp

    """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Workflow Name"),
        help_text=_("The unique name identifier for the workflow process."),
        db_comment="Stores the unique name of the workflow (max 255 characters).",
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Detailed explanation of the workflow's purpose and process."),
        db_comment="Contains detailed textual description of the workflow.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Workflow")
        verbose_name_plural = _("Workflows")

    def __str__(self):
        return self.name
