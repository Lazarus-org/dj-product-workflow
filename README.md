# Welcome to the Django Product Workflow Documentation!

[![License](https://img.shields.io/github/license/lazarus-org/dj-product-workflow)](https://github.com/lazarus-org/dj-product-workflow/blob/main/LICENSE)
[![PyPI Release](https://img.shields.io/pypi/v/dj-product-workflow)](https://pypi.org/project/dj-product-workflow/)
[![Pylint Score](https://img.shields.io/badge/pylint-10/10-brightgreen?logo=python&logoColor=blue)](https://www.pylint.org/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dj-product-workflow)](https://pypi.org/project/dj-product-workflow/)
[![Supported Django Versions](https://img.shields.io/pypi/djversions/dj-product-workflow)](https://pypi.org/project/dj-product-workflow/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow)](https://github.com/pre-commit/pre-commit)
[![Open Issues](https://img.shields.io/github/issues/lazarus-org/dj-product-workflow)](https://github.com/lazarus-org/dj-product-workflow/issues)
[![Last Commit](https://img.shields.io/github/last-commit/lazarus-org/dj-product-workflow)](https://github.com/lazarus-org/dj-product-workflow/commits/main)
[![Languages](https://img.shields.io/github/languages/top/lazarus-org/dj-product-workflow)](https://github.com/lazarus-org/dj-product-workflow)
[![Coverage](https://codecov.io/gh/lazarus-org/dj-product-workflow/branch/main/graph/badge.svg)](https://codecov.io/gh/lazarus-org/dj-product-workflow)

[`dj-product-workflow`](https://github.com/lazarus-org/dj-product-workflow/) is a Django package developed by Lazarus to empower businesses in managing and visualizing product development workflows.
Designed for managers and developers, this package provides a robust framework to define comprehensive workflows, steps, and transition scenarios for products. By preparing workflows just once, teams can create a reusable, structured representation of product logic that’s accessible through intuitive templates and views.

Developers—such as front-end specialists—can explore these workflows to understand the full scope of product scenarios, dependencies, and progression without needing explicit guidance for each case.

With built-in authentication, optimized data retrieval, and extensible design, `dj-product-workflow` simplifies collaboration, enhances clarity, and accelerates development by offering a single source of truth for product processes.


## Project Detail

- Language: Python >= 3.9
- Framework: Django >= 4.2

## Documentation Overview

The documentation is organized into the following sections:

- **[Quick Start](#quick-start)**: Get up and running quickly with basic setup instructions.
- **[Usage](#usage)**: How to effectively use the package in your projects.
- **[Settings](#settings)**: Configuration options and settings you can customize.

---

# Quick Start

This section provides a fast and easy guide to getting the `dj-product-workflow` package up and running in your Django
project.
Follow the steps below to quickly set up the package and start using the package.

## 1. Install the Package

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

```bash
$ pip install dj-product-workflow
```

**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

```bash
$ poetry add dj-product-workflow
```

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

```bash
$ pipenv install dj-product-workflow
```

## 2. Add to Installed Apps

After installing the necessary packages, ensure that `product_workflow` is added to
the `INSTALLED_APPS` in your Django `settings.py` file:

```python
INSTALLED_APPS = [
    # ...
    "product_workflow",
    # ...
]
```

## 3. Apply Migrations

Run the following command to apply the necessary migrations:

```shell
python manage.py migrate
```

## 5. Add Product Workflow URLs

To use the Django Template View for exploring workflows, you should Include necessary urls in your project’s `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path("products/", include("product_workflow.urls")),
    # ...
]
```

# Usage

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of
the Django admin panels for managing product workflows.

**Hint**: To use the package effectively, in the Admin panel, first create a `Product` instance, then a `Workflow` instance. After that, use `ProductWorkflow` as a through table to assign workflows to products. Create an `Step` and assign it as the first step of a workflow via `ProductWorkflow`, then add multiple steps and transitions to define the `from_step` and `to_step` progression and assign the last step as `last_step` in the workflow to be placed at the bottom of the tree. If you want a node (step) to appear at the top of the workflow visualization, set it as the `first_step` in `ProductWorkflow` to position it as the starting point of the tree. Similarly, if you want a node to appear at the bottom, set it as the `last_step` in `ProductWorkflow` to mark it as the endpoint.

**Example**:
1. Create a `Product`:
   - Name: "Product A"
2. Create a `Workflow`:
   - Name: "Authentication Process"
3. Create `Step` instances:
   - Step 1: "check user info" (will be first step)
   - Step 2: "insert password"
   - Step 3: "login verify" (will be last step)
4. Create a `ProductWorkflow`:
   - Product: "Product A"
   - Workflow: "Authentication Process"
   - First Step: "check user info" (positions "check user info" at the top of the graph)
   - Last Step: "login verify" (positions "login verify" at the bottom of the graph)
5. Add `Transition` instances:
   - Transition 1: From "check user info" to "insert password"
   - Transition 2: From "insert password" to "login verify"

In the visualization, "check user info" will be fixed at the top, "login verify" at the bottom, and "insert password" will be positioned between them based on the transitions.

## Admin Site

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your
Django settings. Otherwise, Django may raise the following error during checks or the ModelAdmin will not accessible in
the Admin panel.

To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class
instance

```python
PRODUCT_WORKFLOW_ADMIN_SITE_CLASS = "path.to.your.custom.site"
```

example of a custom Admin Site:

```python
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"


# Instantiate the custom admin site as example
example_admin_site = CustomAdminSite(name="custom_admin")
```

and then reference the instance like this:

```python
product_workflow_ADMIN_SITE_CLASS = "path.to.example_admin_site"
```

This setup allows `dj-product-workflow` to use your custom admin site for its Admin interface, preventing any errors and
ensuring a smooth integration with the custom admin interface.

# Admin Panel

The admin interface in `dj-product-workflow` provides a powerful and intuitive way to manage products, workflows, product-workflow associations, steps, and transitions. Each model is equipped with a customized `ModelAdmin` class to streamline administration tasks. Below are the features and functionalities of each admin interface.

---

## ProductAdmin

The `ProductAdmin` class manages `Product` instances in the Django admin panel.

### List Display
The list view displays:
- **ID**: Unique identifier of the product.
- **Name**: Name of the product.
- **Description**: Description of the product.
- **Created At**: Timestamp of creation.
- **Updated At**: Timestamp of last update.

### Search Functionality
Admins can search by:
- **Name**: Product name.
- **Description**: Product description.

### Filtering
Filter options include:
- **Created At**: Filter by creation date.
- **Updated At**: Filter by last update date.

### Date Hierarchy
- **Created At**: Allows drilling down by creation date.

### Ordering
- Sorted by **Name** in ascending order.

---

## WorkflowAdmin

The `WorkflowAdmin` class manages `Workflow` instances in the Django admin panel.

### List Display
The list view displays:
- **ID**: Unique identifier of the workflow.
- **Name**: Name of the workflow.
- **Created At**: Timestamp of creation.
- **Updated At**: Timestamp of last update.

### Search Functionality
Admins can search by:
- **Name**: Workflow name.
- **Description**: Workflow description (if applicable).

### Filtering
Filter options include:
- **Created At**: Filter by creation date.
- **Updated At**: Filter by last update date.

### Date Hierarchy
- **Created At**: Allows drilling down by creation date.

### Ordering
- Sorted by **Name** in ascending order.

---

## ProductWorkflowAdmin

The `ProductWorkflowAdmin` class manages `ProductWorkflow` instances, linking products to workflows.

### List Display
The list view displays:
- **ID**: Unique identifier of the product-workflow association.
- **Product**: The associated product.
- **Workflow**: The associated workflow.
- **First Step**: The first step in the workflow (if set).
- **Created At**: Timestamp of creation.
- **Updated At**: Timestamp of last update.

### Search Functionality
Admins can search by:
- **Product Name**: Name of the associated product (`product__name`).
- **Workflow Name**: Name of the associated workflow (`workflow__name`).
- **First Step Name**: Name of the first step (`first_step__name`).

### Filtering
Filter options include:
- **Workflow**: Filter by associated workflow.
- **Created At**: Filter by creation date.
- **Updated At**: Filter by last update date.

### Date Hierarchy
- **Created At**: Allows drilling down by creation date.

### Ordering
- Sorted by **Product** and **Workflow** in ascending order.

### Autocomplete Fields
- **Product**: Autocomplete for selecting products.
- **Workflow**: Autocomplete for selecting workflows.
- **First Step**: Autocomplete for selecting the first step.

---

## StepAdmin

The `StepAdmin` class manages `Step` instances within product workflows.

### List Display
The list view displays:
- **ID**: Unique identifier of the step.
- **Name**: Name of the step.
- **Order**: Execution order within the workflow.
- **Workflow**: The associated workflow.
- **Created At**: Timestamp of creation.
- **Updated At**: Timestamp of last update.

### Search Functionality
Admins can search by:
- **Name**: Step name.
- **Description**: Step description.
- **Workflow Name**: Name of the associated workflow (`workflow__name`).

### Filtering
Filter options include:
- **Workflow**: Filter by associated product workflow.
- **Created At**: Filter by creation date.
- **Updated At**: Filter by last update date.

### Date Hierarchy
- **Created At**: Allows drilling down by creation date.

### Ordering
- Sorted by **Workflow** and **Order** in ascending order.

### Autocomplete Fields
- **Workflow**: Autocomplete for selecting the workflow.

---

## TransitionAdmin

The `TransitionAdmin` class manages `Transition` instances between steps in workflows.

### List Display
The list view displays:
- **ID**: Unique identifier of the transition.
- **From Step**: The starting step of the transition.
- **To Step**: The destination step of the transition.
- **Condition**: Optional condition for the transition (if set).
- **Workflow**: The associated product workflow.

### Search Functionality
Admins can search by:
- **Workflow Name**: Name of the associated workflow (`workflow__name`).
- **From Step Name**: Name of the starting step (`from_step__name`).
- **To Step Name**: Name of the destination step (`to_step__name`).

### Filtering
Filter options include:
- **Workflow**: Filter by associated product workflow.

### Ordering
- Sorted by **Workflow**, **From Step**, and **To Step** in ascending order.

### Autocomplete Fields
- **From Step**: Autocomplete for selecting the starting step.
- **To Step**: Autocomplete for selecting the destination step.

### Read-Only Fields
- **Workflow**: The associated workflow (auto-set and non-editable).

---

## View Template Usage

The `dj-product-workflow` package provides two main views—`ProductWorkflowListView` and `ProductWorkflowDetailView`—to display product workflows in a web interface. These views are accessible via specific routes and render data using templates. Below, we explain how to use these templates, their routes, and the context data available for rendering.

---

### ProductWorkflowListView

#### Description
`ProductWorkflowListView` displays a list of all `ProductWorkflow` instances, showing an overview of products and their associated workflows.

#### Route
- **URL**: `/products/product_workflow/`
- **Name**: `product_workflow_list`
- **Access**: Requires authentication (default `LoginRequiredMixin`).

#### Template
- **Name**: `product_workflow_list.html`
- **Location**: This template located in `product_workflow/templates/product_workflow_list.html`.

#### Context Data
- **product_workflows**: A queryset of `ProductWorkflow` objects, with `product` and `workflow` fields preloaded via `select_related` for efficient rendering.

---

### ProductWorkflowDetailView

#### Description
`ProductWorkflowDetailView` displays detailed information about a specific `ProductWorkflow`, including its associated steps and transitions shown as graph.

#### Route
- **URL**: `/products/product_workflow/<int:product_workflow_id>/`
- **Name**: `product_workflow_detail`
- **Access**: Requires authentication (default `LoginRequiredMixin`).
- **Parameter**: `product_workflow_id` (integer) identifies the specific `ProductWorkflow`.

#### Template
- **Name**: `product_workflow_detail.html`
- **Location**: This template is located in `product_workflow/templates/product_workflow_detail.html`.

#### Context Data
- **product_workflow**: The specific `ProductWorkflow` instance, with `product`, `workflow`, and `current_step` preloaded via `select_related`.
- **steps**: A queryset of `Step` objects related to the workflow, ordered by `order`.
- **transitions**: A queryset of `Transition` objects for the workflow, with `from_step` and `to_step` preloaded via `select_related`.

---

# Settings

This section outlines the available settings for configuring the `dj-product-workflow` package. You can customize these
settings in your Django project's `settings.py` file to tailor the behavior of the package to your
needs.

## Example Settings

Below is an example configuration with default values:

```python

PRODUCT_WORKFLOW_ADMIN_SITE_CLASS = None
PRODUCT_WORKFLOW_VIEW_AUTH_MIXIN = "django.contrib.auth.mixins.LoginRequiredMixin"
PRODUCT_WORKFLOW_VIEW_ORDERING_FIELDS = ["product__name", "-created_at"]
```

## Settings Overview

Below is a detailed description of each setting, so you can better understand and tweak them to fit your project's
needs.

---

### `PRODUCT_WORKFLOW_ADMIN_SITE_CLASS`

**Type**: `Optional[str]`

**Default**: `None`

**Description**: Optionally specifies a custom `AdminSite` class to apply to the Admin interface. This allows for more customization of the Admin interface, enabling you to integrate your own `AdminSite` class into the `dj-product-workflow` admin panel.

---

### `PRODUCT_WORKFLOW_VIEW_AUTH_MIXIN`

**Type**: `Optional[str]`

**Default**: `"django.contrib.auth.mixins.LoginRequiredMixin"`

**Description**: Optionally specifies a custom authentication mixin class to apply to template views (e.g., `ProductWorkflowListView` and `ProductWorkflowDetailView`). This setting controls access to the list and detail views, allowing you to enforce custom permission logic tailored to your business needs. By default, it uses Django’s `LoginRequiredMixin`, which restricts access to authenticated users only. You can override this with a custom mixin or another existing Django mixin (e.g., `PermissionRequiredMixin`) to implement more specific access rules.

#### Example: Custom Authentication Mixin

To customize access control, you can define your own mixin or use an existing one. Here’s an example of implementing a custom mixin that restricts access to staff users only, followed by how to configure it:

```python
# myapp/mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class StaffRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and a staff member."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseForbidden("You must be a staff member to access this view.")  # or you can raise django.core.exceptions.PermissionDenied
        return super().dispatch(request, *args, **kwargs)
```

Update your project’s settings to use this custom mixin:

```python
# settings.py
PRODUCT_WORKFLOW_VIEW_AUTH_MIXIN = "myapp.mixins.StaffRequiredMixin"
```

---

### ``PRODUCT_WORKFLOW_VIEW_ORDERING_FIELDS``

**Type**: ``List[str]``

**Default**: ``["product__name", "-created_at"]``

**Description**: Specifies the fields available for ordering in product workflows list view template, allowing the results to be sorted by
these fields. you can see all available fields here:

### All Available Fields

These are all fields that are available for ordering in the product workflow views (e.g., `ProductWorkflowListView`).

- `id`: Unique identifier of the product workflow (orderable).
- `created_at`: Timestamp when the product workflow was created (orderable, filterable).
- `updated_at`: Timestamp when the product workflow was last updated (orderable, filterable).
- `product__name`: Name of the associated product (orderable, searchable).
- `product__created_at`: Creation timestamp of the associated product (orderable).
- `product__updated_at`: Last update timestamp of the associated product (orderable).
- `workflow__name`: Name of the associated workflow (orderable, searchable).
- `workflow__created_at`: Creation timestamp of the associated workflow (orderable).
- `workflow__updated_at`: Last update timestamp of the associated workflow (orderable).
- `first_step__name`: Name of the first step in the workflow (orderable, searchable).
- `first_step__order`: Execution order of the first step in the workflow (orderable).
- `first_step__created_at`: Creation timestamp of the first step (orderable).
- `first_step__updated_at`: Last update timestamp of the first step (orderable).

**Note**: These fields can be used for ordering in ascending order (e.g., `created_at`) or descending order (e.g., `-created_at`) by prefixing with a minus sign. For example, setting `PRODUCT_WORKFLOW_VIEW_ORDERING_FIELDS = ["-created_at"]` in your settings will sort product workflows by creation date in descending order.
----

# Conclusion

We hope this documentation has provided a comprehensive guide to using and understanding the `dj-product-workflow`.

### Final Notes:

- **Version Compatibility**: Ensure your project meets the compatibility requirements for both Django and Python
  versions.
- **Contributions**: Contributions are welcome! Feel free to check out the [Contributing guide](CONTRIBUTING.md) for
  more details.

If you encounter any issues or have feedback, please reach out via
our [GitHub Issues page](https://github.com/lazarus-org/dj-product-workflow/issues).
