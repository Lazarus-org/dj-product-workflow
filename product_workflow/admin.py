from django.contrib import admin
from .models import Product, Workflow, Step, ProductWorkflow, Transition

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('name',)


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('name',)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'name', 'description', 'order', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'workflow__name')
    list_filter = ('workflow', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('workflow', 'order')
    autocomplete_fields = ('workflow',)


@admin.register(ProductWorkflow)
class ProductWorkflowAdmin(admin.ModelAdmin):
    list_display = ('product', 'workflow', 'current_step', 'created_at', 'updated_at')
    search_fields = ('product__name', 'workflow__name', 'current_step__name')
    list_filter = ('workflow', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('product', 'workflow')
    autocomplete_fields = ('product', 'workflow', 'current_step')


@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'from_step', 'to_step', 'condition')
    search_fields = ('workflow__name', 'from_step__name', 'to_step__name')
    list_filter = ('workflow',)
    ordering = ('workflow', 'from_step', 'to_step')
    autocomplete_fields = ('workflow', 'from_step', 'to_step')