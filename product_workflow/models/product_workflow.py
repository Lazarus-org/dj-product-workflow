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
        current_step (Step): The current step in the workflow for this product.
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
    current_step = models.ForeignKey(
        "Step",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Current Step"),
        help_text=_("The current step in the workflow for this product."),
        db_comment="Foreign key reference to the Step model. Can be null if no step is active.",
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
            "<product_id> - <workflow_id> (Current Step: <current_step_name>)"

        - Uses `self.product_id` and `self.workflow_id` to avoid unnecessary queries.
        - Checks `self.current_step_id` before accessing `self.current_step.name`
          to prevent additional database lookups.
        - Defaults `current_step_name` to `"None"` if no current step is assigned.

        Returns:
            str: A human-readable representation of the product workflow.

        """
        current_step_name: str = (
            getattr(self.current_step, "name", "None")
            if self.current_step_id
            else "None"
        )
        return f"Product ID:{self.product_id} - Workflow ID:{self.workflow_id} (Current Step: {current_step_name})"

    def clean(self) -> None:
        """Validates that a product can only be associated with a workflow
        once.

        This method enforces the uniqueness constraint at the application level,
        preventing duplicate `(product, workflow)` pairs before database insertion.

        Steps:
        - Calls `super().clean()` to ensure base model validation is applied.
        - Checks if another `ProductWorkflow` instance exists with the same
          `product` and `workflow`, excluding the current instance (`self`).
        - If a duplicate is found, raises a `ValidationError`.

        Raises:
            ValidationError: If a duplicate `ProductWorkflow` entry exists.

        """
        super().clean()

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
