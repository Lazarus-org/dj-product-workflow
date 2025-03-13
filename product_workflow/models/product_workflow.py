from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from product_workflow.mixins.models.timestamp import TimeStampModel


class ProductWorkflow(TimeStampModel):
    """Represents the association between a product and a workflow, tracking
    its progress.

    Attributes:
        product (Product): The product linked to this workflow.
        workflow (Workflow): The workflow associated with this product.
        first_step (Step): The first step in the workflow for this product.
        last_step (Step): The last step in the workflow for this product.
        created_at (datetime): Auto-generated creation timestamp.
        updated_at (datetime): Auto-generated last modification timestamp.

    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="workflows",
        verbose_name=_("Product"),
        help_text=_("The product associated with this workflow."),
        db_comment="Foreign key reference to the Product model.",
    )
    workflow = models.ForeignKey(
        "Workflow",
        on_delete=models.CASCADE,
        related_name="product_workflows",
        verbose_name=_("Workflow"),
        help_text=_("The workflow associated with this product."),
        db_comment="Foreign key reference to the Workflow model.",
    )
    first_step = models.ForeignKey(
        "Step",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="first_step_workflows",
        verbose_name=_("First Step"),
        help_text=_("The first step in the workflow for this product."),
        db_comment="Foreign key reference to the Step model. Can be null if no step is active.",
    )
    last_step = models.ForeignKey(
        "Step",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_step_workflows",
        verbose_name=_("Last Step"),
        help_text=_("The last step in the workflow for this product."),
        db_comment="Foreign key reference to the Step model. Can be null if no step is defined.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "workflow"],
                name="unique_product_workflow",
                violation_error_message=_(
                    "A product can only be associated with a workflow once."
                ),
            ),
        ]
        verbose_name = _("Product Workflow")
        verbose_name_plural = _("Product Workflows")

    def __str__(self) -> str:
        """Returns a string representation of the product workflow.

        The representation follows the format:
            "<product_id> - <workflow_id> (First: <first_step_name>, Last: <last_step_name>)"

        - Uses `self.product_id` and `self.workflow_id` to avoid unnecessary queries.
        - Checks `self.first_step_id` and `self.last_step_id` before accessing names
          to prevent additional database lookups.
        - Defaults step names to `"None"` if no steps are assigned.

        Returns:
            str: A human-readable representation of the product workflow.

        """
        first_step_name: str = (
            getattr(self.first_step, "name", "None") if self.first_step_id else "None"
        )
        last_step_name: str = (
            getattr(self.last_step, "name", "None") if self.last_step_id else "None"
        )
        return (
            f"Product ID:{self.product_id} - Workflow ID:{self.workflow_id} "
            f"(First: {first_step_name}, Last: {last_step_name})"
        )

    def clean(self) -> None:
        """Validates that a product can only be associated with a workflow once
        and that first_step and last_step belong to the associated workflow.

        This method enforces:
        1. Uniqueness constraint at the application level for (product, workflow) pairs.
        2. Ensures first_step and last_step (if set) belong to the associated workflow.

        Steps:
        - Calls `super().clean()` for base model validation.
        - Checks for duplicate (product, workflow) pairs.
        - Validates that first_step and last_step are part of the workflow's steps.

        Raises:
            ValidationError: If validation fails for uniqueness or step membership.

        """
        super().clean()

        # Check for duplicate product-workflow combination
        if (
            self.workflow_id
            and ProductWorkflow.objects.filter(
                product=self.product, workflow=self.workflow
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {
                    "workflow": _(
                        "A product can only be associated with a workflow once."
                    )
                }
            )

        # Validate that first_step belongs to the workflow
        if (
            self.first_step_id
            and self.workflow_id
            and not self.workflow.steps.filter(id=self.first_step_id).exists()
        ):
            raise ValidationError(
                {
                    "first_step": _(
                        "The first step must belong to the associated workflow."
                    )
                }
            )

        # Validate that last_step belongs to the workflow
        if (
            self.last_step_id
            and self.workflow_id
            and not self.workflow.steps.filter(id=self.last_step_id).exists()
        ):
            raise ValidationError(
                {
                    "last_step": _(
                        "The last step must belong to the associated workflow."
                    )
                }
            )

        if (
            self.first_step_id
            and self.last_step_id
            and self.first_step_id == self.last_step_id
        ):
            raise ValidationError(
                {"last_step": _("The first step and last step cannot be the same.")}
            )
