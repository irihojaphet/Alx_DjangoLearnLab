# Library Project - Advanced Features and Security

This Django project implements custom user authentication and role-based access control using permissions and groups.

## Features

### Custom User Model
- Extended Django's AbstractUser with additional fields:
  - `date_of_birth`: DateField for user's date of birth
  - `profile_photo`: ImageField for user profile photos
- Custom user manager with `create_user` and `create_superuser` methods

### Permissions and Groups System

The application implements a role-based access control (RBAC) system using Django's built-in permissions and groups.

#### Custom Permissions

The `Book` model defines four custom permissions:

- **can_view**: Allows users to view books (read-only access)
- **can_create**: Allows users to create new books
- **can_edit**: Allows users to edit existing books
- **can_delete**: Allows users to delete books

#### User Groups

Three groups are configured with different permission levels:

1. **Viewers**
   - Permissions: `can_view` only
   - Access Level: Read-only
   - Can view books but cannot modify them

2. **Editors**
   - Permissions: `can_view`, `can_create`, `can_edit`
   - Access Level: Read, Create, and Edit
   - Can view, create, and edit books but cannot delete them

3. **Admins**
   - Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
   - Access Level: Full access
   - Complete control over all book operations

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

After setting up the custom user model and permissions:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Set Up Groups

Run the management command to create groups and assign permissions:

```bash
python manage.py setup_groups
```

This will create the Viewers, Editors, and Admins groups with their respective permissions.

### 4. Create Superuser

Create a superuser account for admin access:

```bash
python manage.py createsuperuser
```

### 5. Assign Users to Groups

1. Log in to Django admin at `/admin/`
2. Navigate to Users section
3. Select a user and assign them to the appropriate group(s)
4. Save the user

## Usage

### View Functions

All views in `bookshelf/views.py` are protected with permission decorators:

- `book_list`: Lists all books (requires `can_view`)
- `book_detail`: Shows book details (requires `can_view`)
- `create_book`: Creates a new book (requires `can_create`)
- `edit_book`: Edits an existing book (requires `can_edit`)
- `delete_book`: Deletes a book (requires `can_delete`)

### URL Patterns

- `/bookshelf/` - List all books (requires `can_view`)
- `/bookshelf/<id>/` - View book details (requires `can_view`)
- `/bookshelf/create/` - Create a new book (requires `can_create`)
- `/bookshelf/<id>/edit/` - Edit a book (requires `can_edit`)
- `/bookshelf/<id>/delete/` - Delete a book (requires `can_delete`)

## Testing Permissions

### Test Users Setup

1. Create test users through Django admin or command line
2. Assign each user to a different group:
   - User 1 → Viewers group
   - User 2 → Editors group
   - User 3 → Admins group

### Test Scenarios

1. **As Viewer**:
   - ✅ Can view list of books
   - ✅ Can view individual book details
   - ❌ Cannot create, edit, or delete books (will get 403 Forbidden)

2. **As Editor**:
   - ✅ Can view books
   - ✅ Can create new books
   - ✅ Can edit existing books
   - ❌ Cannot delete books (will get 403 Forbidden)

3. **As Admin**:
   - ✅ Full access to all operations
   - ✅ Can view, create, edit, and delete books

## Project Structure

```
LibraryProject/
├── bookshelf/
│   ├── models.py              # Custom user model and Book model with permissions
│   ├── views.py               # Views with permission checks
│   ├── admin.py               # Admin configuration
│   ├── urls.py                # URL patterns
│   ├── management/
│   │   └── commands/
│   │       └── setup_groups.py  # Command to set up groups
│   └── PERMISSIONS_AND_GROUPS.md  # Detailed documentation
├── relationship_app/          # Additional app with related models
└── LibraryProject/
    ├── settings.py            # Settings with AUTH_USER_MODEL configuration
    └── urls.py                # Main URL configuration
```

## Configuration

### Custom User Model

The project uses a custom user model defined in `bookshelf/models.py`:

```python
AUTH_USER_MODEL = 'bookshelf.CustomUser'
```

This is configured in `settings.py`.

### Media Files

Media files (like profile photos) are served in development mode. The settings include:

```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Documentation

For more detailed information about the permissions and groups system, see:
- `bookshelf/PERMISSIONS_AND_GROUPS.md` - Comprehensive guide on permissions and groups
- Module docstrings in `models.py` and `views.py` - Code-level documentation

## Troubleshooting

### Permissions Not Working

1. Ensure migrations have been run: `python manage.py migrate`
2. Run the setup groups command: `python manage.py setup_groups`
3. Verify user is assigned to the correct group
4. User may need to log out and log back in to refresh permission cache

### 403 Forbidden Errors

If users get 403 errors:
- Verify they have the required permission
- Check that the permission codename matches exactly (case-sensitive)
- Ensure the app label is correct (`bookshelf`)

## Notes

- Superusers automatically have all permissions and bypass permission checks
- Users inherit permissions from their groups
- Individual permissions can also be assigned directly to users
- All views require authentication (`@login_required`)
- Permission checks use `raise_exception=True` to return 403 errors
