import pytest

from product_workflow.models import Product, ProductWorkflow, Step, Workflow, Transition


@pytest.fixture
def product() -> Product:
    """
    Fixture to create a Product instance.
    """
    return Product.objects.create(name="Test Product", description="Test Description")


@pytest.fixture
def workflow() -> Workflow:
    """
    Fixture creating a sample Workflow instance.
    """
    return Workflow.objects.create(name="Test Workflow")


@pytest.fixture
def another_workflow() -> Workflow:
    """
    Fixture creating a sample Workflow instance.
    """
    return Workflow.objects.create(name="Another Workflow")


@pytest.fixture
def product_workflow(product, workflow):
    """
    Fixture creating a sample ProductWorkflow instance with steps.
    """
    product_workflow = ProductWorkflow.objects.create(
        product=product, workflow=workflow
    )

    return product_workflow


@pytest.fixture
def another_product_workflow(product, another_workflow):
    """
    Fixture creating another ProductWorkflow instance.
    """
    return ProductWorkflow.objects.create(product=product, workflow=another_workflow)


@pytest.fixture
def step(workflow) -> Step:
    """
    Fixture creating a sample Step instance linked to a workflow.
    """
    return Step.objects.create(workflow=workflow, name="Step 1", order=1)


@pytest.fixture
def another_step(workflow) -> Step:
    """
    Fixture creating a sample Step instance linked to a workflow.
    """
    return Step.objects.create(workflow=workflow, name="Step 2", order=2)


@pytest.fixture
def step_from_different_workflow(product, workflow):
    """
    Fixture creating a Step linked to a different ProductWorkflow.
    """
    different_workflow = Workflow.objects.create(name="Different Workflow")
    ProductWorkflow.objects.create(product=product, workflow=different_workflow)
    return Step.objects.create(workflow=different_workflow, name="Step X", order=1)


@pytest.fixture
def transition(step, another_step, workflow):
    """
    Fixture creating a sample Transition instance.
    """
    return Transition.objects.create(
        workflow=workflow,
        from_step=step,
        to_step=another_step,
        condition="Test condition",
    )


@pytest.fixture
def product_workflow_for_view(product, workflow):
    """
    Fixture creating a sample ProductWorkflow instance with steps and transitions.
    """
    _product_workflow = ProductWorkflow.objects.create(
        product=product, workflow=workflow
    )
    step1 = Step.objects.create(workflow=workflow, name="Step 1", order=1)
    step2 = Step.objects.create(workflow=workflow, name="Step 2", order=2)
    Transition.objects.create(workflow=workflow, from_step=step1, to_step=step2)
    return _product_workflow
