# Social Media API

A Django REST Framework-based Social Media API with user authentication and profile management.

## Project Overview

This project is the foundation for a Social Media API, focusing on user authentication, registration, and profile management. It uses Django REST Framework for API functionality and token-based authentication.

## Features

- Custom User Model with extended fields (bio, profile_picture, followers)
- User Registration with token generation
- User Login with token authentication
- User Profile Management (GET, PUT, PATCH)
- Post Creation and Management (CRUD operations)
- Comment System for Posts
- Pagination and Filtering for Posts
- Token-based Authentication using Django REST Framework
- Permission-based Access Control (users can only edit/delete their own content)

## Project Structure

```
social_media_api/
├── accounts/              # User authentication app
│   ├── models.py         # Custom User model
│   ├── views.py          # API views (register, login, profile)
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # URL routing
│   └── admin.py          # Admin configuration
├── posts/                 # Posts and comments app
│   ├── models.py         # Post and Comment models
│   ├── views.py          # ViewSets for posts and comments
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # URL routing with routers
│   ├── permissions.py    # Custom permissions
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

## Posts API Endpoints

All posts endpoints require authentication. Base URL: `http://127.0.0.1:8000/api/posts/`

### 1. List Posts

**Endpoint:** `GET /api/posts/`

**Description:** Retrieve a paginated list of all posts. Supports search and filtering.

**Authentication Required:** Yes

**Query Parameters:**
- `search`: Search posts by title or content (e.g., `?search=django`)
- `ordering`: Order results by field (e.g., `?ordering=-created_at`, `?ordering=title`)
- `page`: Page number for pagination (default: 1)

**Response (200 OK):**
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "johndoe",
            "title": "My First Post",
            "content": "This is the content of my first post...",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comments_count": 3
        }
    ]
}
```

### 2. Create Post

**Endpoint:** `POST /api/posts/`

**Description:** Create a new post. The author is automatically set to the authenticated user.

**Authentication Required:** Yes

**Request Body:**
```json
{
    "title": "My First Post",
    "content": "This is the content of my first post..."
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "author": "johndoe",
    "title": "My First Post",
    "content": "This is the content of my first post...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "comments": [],
    "comments_count": 0
}
```

### 3. Retrieve Post

**Endpoint:** `GET /api/posts/{id}/`

**Description:** Retrieve a specific post with all its comments.

**Authentication Required:** Yes

**Response (200 OK):**
```json
{
    "id": 1,
    "author": "johndoe",
    "title": "My First Post",
    "content": "This is the content of my first post...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "comments": [
        {
            "id": 1,
            "post": 1,
            "author": "janedoe",
            "content": "Great post!",
            "created_at": "2024-01-15T11:00:00Z",
            "updated_at": "2024-01-15T11:00:00Z"
        }
    ],
    "comments_count": 1
}
```

### 4. Update Post

**Endpoint:** `PUT /api/posts/{id}/` or `PATCH /api/posts/{id}/`

**Description:** Update a post. Only the post author can update their own posts.

**Authentication Required:** Yes

**Request Body:**
```json
{
    "title": "Updated Post Title",
    "content": "Updated content..."
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "author": "johndoe",
    "title": "Updated Post Title",
    "content": "Updated content...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T12:00:00Z",
    "comments": [],
    "comments_count": 0
}
```

### 5. Delete Post

**Endpoint:** `DELETE /api/posts/{id}/`

**Description:** Delete a post. Only the post author can delete their own posts.

**Authentication Required:** Yes

**Response (204 No Content)**

### 6. Get Post Comments

**Endpoint:** `GET /api/posts/{id}/comments/`

**Description:** Retrieve all comments for a specific post.

**Authentication Required:** Yes

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "post": 1,
        "author": "janedoe",
        "content": "Great post!",
        "created_at": "2024-01-15T11:00:00Z",
        "updated_at": "2024-01-15T11:00:00Z"
    }
]
```

## Comments API Endpoints

All comments endpoints require authentication. Base URL: `http://127.0.0.1:8000/api/comments/`

### 1. List Comments

**Endpoint:** `GET /api/comments/`

**Description:** Retrieve a paginated list of all comments. Can be filtered by post.

**Authentication Required:** Yes

**Query Parameters:**
- `post`: Filter comments by post ID (e.g., `?post=1`)
- `ordering`: Order results by field (e.g., `?ordering=-created_at`)
- `page`: Page number for pagination (default: 1)

**Response (200 OK):**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "post": 1,
            "author": "janedoe",
            "content": "Great post!",
            "created_at": "2024-01-15T11:00:00Z",
            "updated_at": "2024-01-15T11:00:00Z"
        }
    ]
}
```

### 2. Create Comment

**Endpoint:** `POST /api/comments/`

**Description:** Create a new comment on a post. The author is automatically set to the authenticated user.

**Authentication Required:** Yes

**Request Body:**
```json
{
    "post": 1,
    "content": "This is a great post!"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "post": 1,
    "author": "janedoe",
    "content": "This is a great post!",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

### 3. Retrieve Comment

**Endpoint:** `GET /api/comments/{id}/`

**Description:** Retrieve a specific comment.

**Authentication Required:** Yes

**Response (200 OK):**
```json
{
    "id": 1,
    "post": 1,
    "author": "janedoe",
    "content": "This is a great post!",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

### 4. Update Comment

**Endpoint:** `PUT /api/comments/{id}/` or `PATCH /api/comments/{id}/`

**Description:** Update a comment. Only the comment author can update their own comments.

**Authentication Required:** Yes

**Request Body:**
```json
{
    "content": "Updated comment content"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "post": 1,
    "author": "janedoe",
    "content": "Updated comment content",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
}
```

### 5. Delete Comment

**Endpoint:** `DELETE /api/comments/{id}/`

**Description:** Delete a comment. Only the comment author can delete their own comments.

**Authentication Required:** Yes

**Response (204 No Content)**

## Pagination

All list endpoints support pagination with a default page size of 10 items. The response includes:
- `count`: Total number of items
- `next`: URL to the next page (null if last page)
- `previous`: URL to the previous page (null if first page)
- `results`: Array of items for the current page

**Example:**
```
GET /api/posts/?page=2
```

## Filtering and Search

### Post Search

Search posts by title or content:
```
GET /api/posts/?search=django
```

### Post Ordering

Order posts by different fields:
```
GET /api/posts/?ordering=-created_at  # Newest first
GET /api/posts/?ordering=title        # Alphabetical by title
GET /api/posts/?ordering=created_at   # Oldest first
```

### Comment Filtering

Filter comments by post:
```
GET /api/comments/?post=1
```

## Permissions

- **Read Operations**: All authenticated users can view posts and comments
- **Create Operations**: All authenticated users can create posts and comments
- **Update/Delete Operations**: Only the author of a post or comment can update or delete it

## Testing Posts and Comments with Postman

### 1. Create a Post

1. Create a POST request to `http://127.0.0.1:8000/api/posts/`
2. Set Headers:
   - `Content-Type: application/json`
   - `Authorization: Token <your_token_here>`
3. Add JSON body:
   ```json
   {
       "title": "My First Post",
       "content": "This is my first post content"
   }
   ```
4. Send request

### 2. List Posts

1. Create a GET request to `http://127.0.0.1:8000/api/posts/`
2. Set Headers:
   - `Authorization: Token <your_token_here>`
3. Optionally add query parameters:
   - `?search=django` - Search posts
   - `?ordering=-created_at` - Order by newest first
   - `?page=1` - Page number
4. Send request

### 3. Create a Comment

1. Create a POST request to `http://127.0.0.1:8000/api/comments/`
2. Set Headers:
   - `Content-Type: application/json`
   - `Authorization: Token <your_token_here>`
3. Add JSON body:
   ```json
   {
       "post": 1,
       "content": "This is a great post!"
   }
   ```
4. Send request

### 4. Update a Post

1. Create a PUT or PATCH request to `http://127.0.0.1:8000/api/posts/1/`
2. Set Headers:
   - `Content-Type: application/json`
   - `Authorization: Token <your_token_here>`
3. Add JSON body with fields to update
4. Send request

### 5. Delete a Comment

1. Create a DELETE request to `http://127.0.0.1:8000/api/comments/1/`
2. Set Headers:
   - `Authorization: Token <your_token_here>`
3. Send request

## Next Steps

Future enhancements may include:

- Like/unlike functionality for posts and comments
- Follow/unfollow endpoints
- User search and discovery
- Media upload handling for posts
- Post categories and tags
- Notifications system

## License

This project is part of a learning curriculum.

## Author

Developed as part of the ALX Django Learning Lab curriculum.

