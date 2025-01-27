from django.shortcuts import render, get_object_or_404
from .models import ProductWorkflow, Transition

def product_workflow_detail(request, product_workflow_id):
    product_workflow = get_object_or_404(ProductWorkflow, id=product_workflow_id)
    steps = product_workflow.workflow.steps.all().order_by('order')
    transitions = Transition.objects.filter(workflow=product_workflow.workflow)

    return render(request, 'detail.html', {
        'product_workflow': product_workflow,
        'steps': steps,
        'transitions': transitions,
    })