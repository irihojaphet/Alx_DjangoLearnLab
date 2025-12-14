# Social Media API

A Django REST Framework-based Social Media API with user authentication and profile management.

## Project Overview

This project is the foundation for a Social Media API, focusing on user authentication, registration, and profile management. It uses Django REST Framework for API functionality and token-based authentication.

## Features

- Custom User Model with extended fields (bio, profile_picture, followers)
- User Registration with token generation
- User Login with token authentication
- User Profile Management (GET, PUT, PATCH)
- Token-based Authentication using Django REST Framework

## Project Structure

```
social_media_api/
├── accounts/              # User authentication app
│   ├── models.py         # Custom User model
│   ├── views.py          # API views (register, login, profile)
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # URL routing
│   └── admin.py          # Admin configuration
├── social_media_api/      # Project settings
│   ├── settings.py       # Django configuration
│   └── urls.py           # Root URL configuration
└── manage.py             # Django management script
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install django djangorestframework Pillow
```

### Step 2: Database Setup

Run migrations to create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser (Optional)

Create an admin user to access the Django admin panel:

```bash
python manage.py createsuperuser
```

### Step 4: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### 1. User Registration

**Endpoint:** `POST /register/`

**Description:** Register a new user account. Returns an authentication token upon successful registration.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": null
}
```

**Response (201 Created):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

### 2. User Login

**Endpoint:** `POST /login/`

**Description:** Authenticate a user and retrieve an authentication token.

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

### 3. User Profile

**Endpoint:** `GET /profile/` or `PUT /profile/` or `PATCH /profile/`

**Description:** Retrieve or update the authenticated user's profile.

**Authentication Required:** Yes (Token Authentication)

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**GET Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": null,
    "followers_count": 5,
    "following_count": 3,
    "date_joined": "2024-01-15T10:30:00Z"
}
```

**PUT/PATCH Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Updated bio",
    "email": "newemail@example.com"
}
```

**PUT/PATCH Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Updated bio",
    "profile_picture": null,
    "followers_count": 5,
    "following_count": 3,
    "date_joined": "2024-01-15T10:30:00Z"
}
```

## User Model

The custom User model extends Django's `AbstractUser` and includes:

- **bio**: TextField for user biography (optional)
- **profile_picture**: ImageField for profile picture (optional)
- **followers**: ManyToMany relationship to other users (asymmetric)

### Key Features:

- Username and email authentication
- Password hashing and validation
- Token-based authentication
- Follower/following relationships

## Testing with Postman

### 1. Register a New User

1. Create a new POST request to `http://127.0.0.1:8000/register/`
2. Set Headers: `Content-Type: application/json`
3. Add JSON body with user details
4. Send request
5. Copy the token from the response

### 2. Login

1. Create a new POST request to `http://127.0.0.1:8000/login/`
2. Set Headers: `Content-Type: application/json`
3. Add JSON body with username and password
4. Send request
5. Copy the token from the response

### 3. Access Profile

1. Create a GET request to `http://127.0.0.1:8000/profile/`
2. Set Headers:
   - `Content-Type: application/json`
   - `Authorization: Token <your_token_here>`
3. Send request

### 4. Update Profile

1. Create a PUT or PATCH request to `http://127.0.0.1:8000/profile/`
2. Set Headers:
   - `Content-Type: application/json`
   - `Authorization: Token <your_token_here>`
3. Add JSON body with fields to update
4. Send request

## Authentication

The API uses Token Authentication. Include the token in the Authorization header for protected endpoints:

```
Authorization: Token <your_token_here>
```

Tokens are automatically generated upon registration and login. Each user has one token that can be used for all authenticated requests.

## Configuration

### Settings

Key configurations in `settings.py`:

- **AUTH_USER_MODEL**: Set to `'accounts.User'` for custom user model
- **REST_FRAMEWORK**: Configured with Token Authentication
- **INSTALLED_APPS**: Includes `rest_framework`, `rest_framework.authtoken`, and `accounts`

### Default Permissions

By default, all API endpoints require authentication except:
- `/register/` - Public access
- `/login/` - Public access

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

## Next Steps

This is the foundation for the Social Media API. Future enhancements may include:

- Post creation and management
- Comments system
- Like/unlike functionality
- Follow/unfollow endpoints
- User search and discovery
- Media upload handling

## License

This project is part of a learning curriculum.

## Author

Developed as part of the ALX Django Learning Lab curriculum.

