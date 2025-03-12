from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from product_workflow.mixins.models.timestamp import TimeStampModel


class Transition(TimeStampModel):
    """Represents a transition between two steps in a workflow.

    Attributes:
        workflow (Workflow): The Workflow this transition belongs to (auto-set).
        from_step (Step): The step this transition starts from.
        to_step (Step): The step this transition leads to.
        condition (str): An optional condition for this transition.

    """

    workflow = models.ForeignKey(
        "Workflow",
        on_delete=models.CASCADE,
        related_name="transitions",
        verbose_name=_("Workflow"),
        help_text=_(
            "The workflow this transition belongs to (automatically set from steps)."
        ),
        db_comment="Foreign key reference to the Workflow model.",
    )
    from_step = models.ForeignKey(
        "Step",
        on_delete=models.CASCADE,
        related_name="outgoing_transitions",
        verbose_name=_("From Step"),
        help_text=_("The step this transition starts from."),
        db_comment="Foreign key reference to the Step model (source step).",
    )
    to_step = models.ForeignKey(
        "Step",
        on_delete=models.CASCADE,
        related_name="incoming_transitions",
        verbose_name=_("To Step"),
        help_text=_("The step this transition leads to."),
        db_comment="Foreign key reference to the Step model (destination step).",
    )
    condition = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Condition"),
        help_text=_(
            "An optional condition for this transition (e.g., a rule or logic)."
        ),
        db_comment="Optional condition or rule for the transition. Can be null if no condition is required.",
    )

    class Meta:
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")
        constraints = [
            models.UniqueConstraint(
                fields=["workflow", "from_step", "to_step"],
                name="unique_transition_per_workflow",
                violation_error_message=_(
                    "A transition between the same steps in a workflow must be unique."
                ),
            ),
        ]

    def __str__(self) -> str:
        """Returns a string representation of the transition.

        The representation follows the format:
            "<from_step_name> -> <to_step_name> (Workflow ID: <workflow_id>)"

        - If `from_step` or `to_step` is `None`, it defaults to "Unknown".
        - Uses `workflow_id` instead of `workflow.name` to avoid unnecessary queries.

        Returns:
            str: A human-readable representation of the transition.

        """
        from_step_name: str = (
            getattr(self.from_step, "name", "Unknown")
            if self.from_step_id
            else "Unknown"
        )
        to_step_name: str = (
            getattr(self.to_step, "name", "Unknown") if self.to_step_id else "Unknown"
        )
        return f"{from_step_name} -> {to_step_name} (Workflow ID: {self.workflow_id})"

    def clean(self) -> None:
        """Validates and sets the `workflow` based on `from_step` and
        `to_step`.

        Ensures:
        - `from_step` and `to_step` belong to the same `workflow`.
        - `workflow` is automatically set to `from_step.workflow` if not provided.
        - Raises an error if `from_step` and `to_step` have mismatched workflows.

        Raises:
            ValidationError: If steps don't belong to the same workflow or if required fields are missing.

        """
        # Check if both steps are provided
        if not self.from_step_id or not self.to_step_id:
            raise ValidationError(
                {
                    "from_step" if not self.from_step_id else "to_step": _(
                        "Both 'From Step' and 'To Step' must be specified."
                    )
                }
            )

        if self.from_step_id == self.to_step_id:
            raise ValidationError(
                {"to_step": _("The from step and to step cannot be the same.")}
            )

        # Fetch the workflows from the steps
        from_step_workflow = getattr(self.from_step, "workflow", None)
        to_step_workflow = getattr(self.to_step, "workflow", None)

        # Validate that both steps belong to the same workflow
        if from_step_workflow != to_step_workflow:
            raise ValidationError(
                _("'From Step' and 'To Step' must belong to the same workflow.")
            )

        # Automatically set workflow if not provided or if it differs
        if not self.workflow_id or self.workflow != from_step_workflow:
            self.workflow = from_step_workflow

        # Validate unique constraint at the application level
        if self.workflow_id:
            existing_transition = Transition.objects.filter(
                workflow=self.workflow,
                from_step=self.from_step,
                to_step=self.to_step,
            ).exclude(
                pk=self.pk
            )  # Exclude current instance if updating

            if existing_transition.exists():
                raise ValidationError(
                    _(
                        "A transition between these steps already exists for this workflow."
                    )
                )
