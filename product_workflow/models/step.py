from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from product_workflow.mixins.models.timestamp import TimeStampModel


class Step(TimeStampModel):
    """Represents an individual step within a workflow process.

    Attributes:
        workflow (Workflow): Workflow containing this step
        name (str): Name of the step (unique within parent workflow)
        description (str): Detailed instructions for completing the step
        order (int): Position of the step in workflow execution sequence
        created_at (datetime): Auto-generated creation timestamp
        updated_at (datetime): Auto-generated last modification timestamp

    """

    workflow = models.ForeignKey(
        "Workflow",
        on_delete=models.CASCADE,
        related_name="steps",
        verbose_name=_("Workflow"),
        help_text=_("The workflow process that contains this step."),
        db_comment="Foreign key reference to the Workflow model.",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Step Name"),
        help_text=_("The name of the step (must be unique within its workflow)."),
        db_comment="Stores the name of the step within its workflow (max 255 chars).",
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Detailed instructions and requirements for completing the step."),
        db_comment="Contains detailed textual description of the step's process.",
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Execution Order"),
        help_text=_(
            "Numerical position in the workflow's execution sequence (starts at 0)."
        ),
        db_comment="Determines the execution sequence order within the workflow.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workflow", "name"],
                name="unique_step_name_per_workflow",
                violation_error_message=_("Step name must be unique within a workflow"),
            ),
            models.UniqueConstraint(
                fields=["workflow", "order"],
                name="unique_step_order_per_workflow",
                violation_error_message=_(
                    "Execution order must be unique within a workflow"
                ),
            ),
        ]
        verbose_name = _("Workflow Step")
        verbose_name_plural = _("Workflow Steps")
        ordering = ["workflow", "order"]

    def __str__(self):
        """Returns a string representation of the step."""
        return f"{self.name} (Order: {self.order})"

    def clean(self):
        """Custom validation to enforce model constraints beyond database-level
        checks."""
        super().clean()

        # Validate unique step name per workflow
        if self.workflow_id:
            existing_steps = Step.objects.filter(
                workflow_id=self.workflow_id, name=self.name
            ).exclude(
                pk=self.pk
            )  # Exclude current instance if updating

            if existing_steps.exists():
                raise ValidationError(
                    {
                        "name": _(
                            "An step with this name already exists in the workflow."
                        )
                    }
                )

        # Validate unique order per workflow
        if self.workflow_id:
            existing_orders = Step.objects.filter(
                workflow_id=self.workflow_id, order=self.order
            ).exclude(
                pk=self.pk
            )  # Exclude current instance if updating

            if existing_orders.exists():
                raise ValidationError(
                    {
                        "order": _(
                            "An step with this execution order already exists in the workflow."
                        )
                    }
                )
