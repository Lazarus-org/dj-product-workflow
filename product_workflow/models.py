from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(
        max_length=255, 
        unique=True, 
        help_text=_("The name of the product.")
    )
    description = models.TextField(
        blank=True, 
        help_text=_("A detailed description of the product.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        db_table_comment = _("Table for storing products")


class Workflow(models.Model):
    name = models.CharField(
        max_length=255, 
        unique=True, 
        help_text=_("The name of the workflow.")
    )
    description = models.TextField(
        blank=True, 
        help_text=_("A detailed description of the workflow.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Workflow")
        verbose_name_plural = _("Workflows")
        db_table_comment = _("Table for storing workflows")


class Step(models.Model):
    workflow = models.ForeignKey(
        Workflow, 
        on_delete=models.CASCADE, 
        related_name='steps', 
        help_text=_("The workflow this step belongs to.")
    )
    name = models.CharField(
        max_length=255, 
        help_text=_("The name of the step.")
    )
    description = models.TextField(
        blank=True, 
        help_text=_("A detailed description of the step.")
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text=_("The order of the step in the workflow.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.workflow.name} - {self.name} (Order: {self.order})"

    class Meta:
        ordering = ['workflow', 'order']
        constraints = [
            UniqueConstraint(fields=['workflow', 'name'], name='unique_step_name_per_workflow'),
            UniqueConstraint(fields=['workflow', 'order'], name='unique_step_order_per_workflow'),
        ]
        verbose_name = _("Step")
        verbose_name_plural = _("Steps")
        db_table_comment = _("Table for storing steps in workflows")


class ProductWorkflow(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='workflows', 
        help_text=_("The product associated with this workflow.")
    )
    workflow = models.ForeignKey(
        Workflow, 
        on_delete=models.CASCADE, 
        related_name='product_workflows', 
        help_text=_("The workflow associated with this product.")
    )
    current_step = models.ForeignKey(
        Step, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text=_("The current step in the workflow for this product.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.workflow.name} (Current Step: {self.current_step.name if self.current_step else 'None'})"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'workflow'], name='unique_product_workflow'),
        ]
        verbose_name = _("Product Workflow")
        verbose_name_plural = _("Product Workflows")
        db_table_comment = _("Table for storing product workflows")


class Transition(models.Model):
    workflow = models.ForeignKey(
        Workflow, 
        on_delete=models.CASCADE, 
        related_name='transitions', 
        help_text=_("The workflow this transition belongs to.")
    )
    from_step = models.ForeignKey(
        Step, 
        on_delete=models.CASCADE, 
        related_name='outgoing_transitions', 
        help_text=_("The step this transition starts from.")
    )
    to_step = models.ForeignKey(
        Step, 
        on_delete=models.CASCADE, 
        related_name='incoming_transitions', 
        help_text=_("The step this transition leads to.")
    )
    condition = models.TextField(
        blank=True, 
        null=True, 
        help_text=_("An optional condition for this transition.")
    )

    def __str__(self):
        return f"{self.from_step.name} -> {self.to_step.name} (Workflow: {self.workflow.name})"

    def clean(self):
        if self.from_step.workflow != self.workflow or self.to_step.workflow != self.workflow:
            raise ValidationError(_("Both steps must belong to the same workflow."))

    class Meta:
        constraints = [
            UniqueConstraint(fields=['workflow', 'from_step', 'to_step'], name='unique_transition_per_workflow'),
        ]
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")
        db_table_comment = _("Table for storing workflow transitions")
