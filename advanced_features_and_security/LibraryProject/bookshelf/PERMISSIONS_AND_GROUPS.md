# Permissions and Groups Setup Guide

This document explains how permissions and groups are configured and used in the Django application.

## Overview

The application implements a role-based access control (RBAC) system using Django's built-in permissions and groups. This allows administrators to control user access to different parts of the application based on their assigned roles.

## Custom Permissions

The `Book` model in `bookshelf/models.py` defines four custom permissions:

- **can_view**: Allows users to view books (read-only access)
- **can_create**: Allows users to create new books
- **can_edit**: Allows users to edit existing books
- **can_delete**: Allows users to delete books

These permissions are defined in the `Book` model's `Meta` class:

```python
class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
```

## Groups

Three groups are set up to manage user permissions:

### 1. Viewers
- **Permissions**: `can_view` only
- **Access Level**: Read-only
- **Use Case**: Users who only need to view books without the ability to modify them

### 2. Editors
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Access Level**: Read, Create, and Edit
- **Use Case**: Content managers who can create and edit books but cannot delete them

### 3. Admins
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access Level**: Full access (all permissions)
- **Use Case**: Administrators who need complete control over books

## Setting Up Groups

### Initial Setup

To create the groups and assign permissions, run the management command:

```bash
python manage.py setup_groups
```

This command will:
1. Create the Viewers, Editors, and Admins groups if they don't exist
2. Assign the appropriate permissions to each group
3. Display a success message confirming the setup

### Manual Setup via Django Admin

Alternatively, you can set up groups manually through Django's admin interface:

1. Navigate to `/admin/auth/group/`
2. Click "Add Group"
3. Enter the group name (e.g., "Viewers")
4. Select the appropriate permissions from the "Available permissions" list
5. Click "Save"

## Assigning Users to Groups

### Via Django Admin

1. Navigate to `/admin/bookshelf/customuser/`
2. Click on a user
3. Scroll to the "Groups" section
4. Select one or more groups for the user
5. Click "Save"

### Programmatically

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
user = User.objects.get(username='example_user')
group = Group.objects.get(name='Editors')
user.groups.add(group)
```

## Permission Enforcement in Views

All views in `bookshelf/views.py` use permission decorators to enforce access control:

### List and Detail Views (Read Access)

```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    # View implementation
```

### Create View

```python
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # View implementation
```

### Edit View

```python
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    # View implementation
```

### Delete View

```python
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    # View implementation
```

## Testing Permissions

### Step 1: Create Test Users

1. Create users through Django admin or using the management command
2. Create users with different usernames (e.g., `viewer1`, `editor1`, `admin1`)

### Step 2: Assign Users to Groups

Assign each user to their respective group:
- `viewer1` → Viewers group
- `editor1` → Editors group
- `admin1` → Admins group

### Step 3: Test Access

1. **As Viewer**: Log in as `viewer1`
   - ✅ Should be able to view the list of books
   - ✅ Should be able to view individual book details
   - ❌ Should NOT be able to create, edit, or delete books
   - If attempting to access restricted views, should get a 403 Forbidden error

2. **As Editor**: Log in as `editor1`
   - ✅ Should be able to view books
   - ✅ Should be able to create new books
   - ✅ Should be able to edit existing books
   - ❌ Should NOT be able to delete books
   - Should get 403 Forbidden when attempting to delete

3. **As Admin**: Log in as `admin1`
   - ✅ Should have full access to all operations
   - ✅ Should be able to view, create, edit, and delete books

### Step 4: Verify Permission Denials

When a user without the required permission tries to access a restricted view:
- They will receive a `403 Forbidden` error (due to `raise_exception=True`)
- The user will not be able to perform the restricted action

## URL Patterns

The following URL patterns are available (all require login and appropriate permissions):

- `/bookshelf/` - List all books (requires `can_view`)
- `/bookshelf/<id>/` - View book details (requires `can_view`)
- `/bookshelf/create/` - Create a new book (requires `can_create`)
- `/bookshelf/<id>/edit/` - Edit a book (requires `can_edit`)
- `/bookshelf/<id>/delete/` - Delete a book (requires `can_delete`)

## Important Notes

1. **Migration Required**: After adding custom permissions to the model, run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Permission Codename**: When checking permissions in code, use the format: `app_label.permission_codename` (e.g., `bookshelf.can_view`)

3. **Superuser Override**: Superusers automatically have all permissions and bypass permission checks

4. **Group Permissions**: Users inherit permissions from their groups. You can also assign individual permissions directly to users.

5. **Permission Cache**: Django caches permissions per request. After assigning a user to a group or permission, the user may need to log out and log back in for changes to take effect.

## Troubleshooting

### Permissions Not Working

1. Verify migrations have been run: `python manage.py migrate`
2. Check that groups exist and have correct permissions: `python manage.py setup_groups`
3. Verify user is assigned to the correct group
4. Ensure user is logged in (permission checks require authentication)
5. Try logging out and logging back in to refresh permission cache

### Permission Denied Errors

If users get 403 errors even with correct permissions:
- Check that the permission codename matches exactly (case-sensitive)
- Verify the app label is correct (should be `bookshelf`)
- Ensure the user's groups haven't been accidentally removed

