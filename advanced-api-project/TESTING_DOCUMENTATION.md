# API Testing Documentation

This document provides comprehensive documentation for the unit tests implemented for the Book API endpoints.

## Table of Contents

1. [Overview](#overview)
2. [Test Structure](#test-structure)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Test Cases](#test-cases)
6. [Interpreting Test Results](#interpreting-test-results)
7. [Best Practices](#best-practices)

## Overview

The test suite for the Book API is located in `/api/test_views.py` and uses Django REST Framework's `APITestCase` for comprehensive API endpoint testing. The tests cover:

- **CRUD Operations**: Create, Read, Update, Delete operations
- **Filtering**: Testing filter capabilities by title, author, and publication_year
- **Searching**: Testing search functionality across title and author fields
- **Ordering**: Testing ordering capabilities by various fields
- **Permissions**: Testing authentication and authorization requirements
- **Validation**: Testing data validation rules
- **Error Handling**: Testing error responses for invalid requests

## Test Structure

### Test Classes

The test suite is organized into the following test classes:

1. **`BookAPITestCase`**: Base test case that sets up test data
2. **`BookListViewTests`**: Tests for listing and querying books
3. **`BookDetailViewTests`**: Tests for retrieving individual books
4. **`BookCreateViewTests`**: Tests for creating new books
5. **`BookUpdateViewTests`**: Tests for updating existing books
6. **`BookDeleteViewTests`**: Tests for deleting books

### Test Data Setup

Each test class inherits from `BookAPITestCase`, which automatically sets up:

- **Test Authors**: Two authors (George Orwell and J.K. Rowling)
- **Test Books**: Three books with different attributes
- **Test User**: A user account for authentication testing

## Running Tests

### Run All Tests

To run all API tests:

```bash
python manage.py test api
```

### Run Specific Test Class

To run tests for a specific view:

```bash
# List view tests
python manage.py test api.test_views.BookListViewTests

# Create view tests
python manage.py test api.test_views.BookCreateViewTests

# Update view tests
python manage.py test api.test_views.BookUpdateViewTests

# Delete view tests
python manage.py test api.test_views.BookDeleteViewTests

# Detail view tests
python manage.py test api.test_views.BookDetailViewTests
```

### Run Specific Test Method

To run a single test method:

```bash
python manage.py test api.test_views.BookListViewTests.test_list_books_public_access
```

### Verbose Output

To see detailed test output:

```bash
python manage.py test api -v 2
```

### Keep Test Database

To keep the test database after running tests (for debugging):

```bash
python manage.py test api --keepdb
```

## Test Coverage

### Total Tests: 26

#### BookListViewTests (13 tests)
- Public access to book list
- Response data structure validation
- Filtering by title, author, and publication_year
- Searching by title and author name
- Ordering by title (ascending/descending)
- Ordering by publication_year (ascending/descending)
- Combined filter, search, and order operations

#### BookDetailViewTests (2 tests)
- Public access to book details
- Handling non-existent book IDs (404 error)

#### BookCreateViewTests (4 tests)
- Authentication requirement
- Creating books with valid data
- Validation of future publication years
- Handling missing required fields

#### BookUpdateViewTests (5 tests)
- Authentication requirement
- Full update (PUT)
- Partial update (PATCH)
- Validation of future publication years
- Handling non-existent book IDs (404 error)

#### BookDeleteViewTests (3 tests)
- Authentication requirement
- Deleting books successfully
- Handling non-existent book IDs (404 error)

## Test Cases

### BookListViewTests

#### test_list_books_public_access
**Purpose**: Verify that unauthenticated users can access the book list.

**What it tests**:
- Endpoint returns 200 OK
- All books are returned in the response

**Expected Result**: ✅ Pass

#### test_filter_by_title
**Purpose**: Test filtering books by exact title match.

**What it tests**:
- Filtering with `?title=1984` returns only matching books
- Response contains exactly one book

**Expected Result**: ✅ Pass

#### test_filter_by_author
**Purpose**: Test filtering books by author ID.

**What it tests**:
- Filtering with `?author=1` returns only books by that author
- All returned books belong to the specified author

**Expected Result**: ✅ Pass

#### test_filter_by_publication_year
**Purpose**: Test filtering books by publication year.

**What it tests**:
- Filtering with `?publication_year=1949` returns only books from that year
- Response contains books with matching publication year

**Expected Result**: ✅ Pass

#### test_search_by_title
**Purpose**: Test searching books by title using the search parameter.

**What it tests**:
- Searching with `?search=1984` finds books with matching titles
- Search is case-insensitive and supports partial matches

**Expected Result**: ✅ Pass

#### test_search_by_author_name
**Purpose**: Test searching books by author name.

**What it tests**:
- Searching with `?search=Orwell` finds books by authors with matching names
- Search works across related fields (author__name)

**Expected Result**: ✅ Pass

#### test_ordering_by_title_ascending
**Purpose**: Test ordering books by title in ascending order.

**What it tests**:
- Ordering with `?ordering=title` returns books alphabetically
- Titles are in ascending order

**Expected Result**: ✅ Pass

#### test_ordering_by_title_descending
**Purpose**: Test ordering books by title in descending order.

**What it tests**:
- Ordering with `?ordering=-title` returns books in reverse alphabetical order
- Titles are in descending order

**Expected Result**: ✅ Pass

#### test_ordering_by_publication_year_ascending
**Purpose**: Test ordering books by publication year (oldest first).

**What it tests**:
- Ordering with `?ordering=publication_year` returns books from oldest to newest
- Years are in ascending order

**Expected Result**: ✅ Pass

#### test_ordering_by_publication_year_descending
**Purpose**: Test ordering books by publication year (newest first).

**What it tests**:
- Ordering with `?ordering=-publication_year` returns books from newest to oldest
- Years are in descending order

**Expected Result**: ✅ Pass

#### test_combined_filter_search_order
**Purpose**: Test combining filtering, searching, and ordering in a single request.

**What it tests**:
- Multiple query parameters work together correctly
- Results are filtered, searched, and ordered as expected

**Expected Result**: ✅ Pass

### BookDetailViewTests

#### test_retrieve_book_public_access
**Purpose**: Verify that unauthenticated users can retrieve a single book.

**What it tests**:
- Endpoint returns 200 OK
- Response contains correct book data (id, title, publication_year, author)

**Expected Result**: ✅ Pass

#### test_retrieve_nonexistent_book
**Purpose**: Test retrieving a book that doesn't exist.

**What it tests**:
- Endpoint returns 404 Not Found for non-existent book IDs
- Error handling works correctly

**Expected Result**: ✅ Pass

### BookCreateViewTests

#### test_create_book_requires_authentication
**Purpose**: Verify that unauthenticated users cannot create books.

**What it tests**:
- Endpoint returns 401 Unauthorized or 403 Forbidden
- Authentication is required for creating books

**Expected Result**: ✅ Pass

#### test_create_book_authenticated
**Purpose**: Test creating a book with valid data when authenticated.

**What it tests**:
- Endpoint returns 201 Created
- Book is created in the database
- Response contains correct book data
- Success message is included

**Expected Result**: ✅ Pass

#### test_create_book_validation_future_year
**Purpose**: Test that creating a book with a future publication year is rejected.

**What it tests**:
- Endpoint returns 400 Bad Request
- Validation error message is returned
- Book is not created in the database

**Expected Result**: ✅ Pass

#### test_create_book_missing_fields
**Purpose**: Test that creating a book with missing required fields is rejected.

**What it tests**:
- Endpoint returns 400 Bad Request
- Validation errors are returned for missing fields

**Expected Result**: ✅ Pass

### BookUpdateViewTests

#### test_update_book_requires_authentication
**Purpose**: Verify that unauthenticated users cannot update books.

**What it tests**:
- Endpoint returns 401 Unauthorized or 403 Forbidden
- Authentication is required for updating books

**Expected Result**: ✅ Pass

#### test_update_book_put_authenticated
**Purpose**: Test updating a book with PUT (full update) when authenticated.

**What it tests**:
- Endpoint returns 200 OK
- All fields are updated correctly
- Book is updated in the database
- Success message is included

**Expected Result**: ✅ Pass

#### test_update_book_patch_authenticated
**Purpose**: Test updating a book with PATCH (partial update) when authenticated.

**What it tests**:
- Endpoint returns 200 OK
- Only specified fields are updated
- Other fields remain unchanged
- Book is updated in the database

**Expected Result**: ✅ Pass

#### test_update_book_validation_future_year
**Purpose**: Test that updating a book with a future publication year is rejected.

**What it tests**:
- Endpoint returns 400 Bad Request
- Validation error message is returned
- Book is not updated in the database

**Expected Result**: ✅ Pass

#### test_update_nonexistent_book
**Purpose**: Test updating a book that doesn't exist.

**What it tests**:
- Endpoint returns 404 Not Found for non-existent book IDs
- Error handling works correctly

**Expected Result**: ✅ Pass

### BookDeleteViewTests

#### test_delete_book_requires_authentication
**Purpose**: Verify that unauthenticated users cannot delete books.

**What it tests**:
- Endpoint returns 401 Unauthorized or 403 Forbidden
- Authentication is required for deleting books

**Expected Result**: ✅ Pass

#### test_delete_book_authenticated
**Purpose**: Test deleting a book when authenticated.

**What it tests**:
- Endpoint returns 204 No Content
- Book is deleted from the database
- Success message is included

**Expected Result**: ✅ Pass

#### test_delete_nonexistent_book
**Purpose**: Test deleting a book that doesn't exist.

**What it tests**:
- Endpoint returns 404 Not Found for non-existent book IDs
- Error handling works correctly

**Expected Result**: ✅ Pass

## Interpreting Test Results

### Successful Test Run

```
Ran 26 tests in 138.284s

OK
```

This indicates all tests passed successfully.

### Failed Test

```
FAIL: test_create_book_requires_authentication (api.test_views.BookCreateViewTests.test_create_book_requires_authentication)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AssertionError: 403 != 401
```

This indicates a test failure. The test expected status code 401 but received 403.

### Error in Test

```
ERROR: test_list_books_public_access (api.test_views.BookListViewTests.test_list_books_public_access)
----------------------------------------------------------------------
Traceback (most last):
  ...
TypeError: 'str' object is not callable
```

This indicates an error occurred during test execution, not a test failure.

## Best Practices

### Writing Tests

1. **Test One Thing**: Each test should verify one specific behavior
2. **Clear Test Names**: Use descriptive names that explain what is being tested
3. **Arrange-Act-Assert**: Structure tests with setup, action, and verification
4. **Isolation**: Tests should be independent and not rely on execution order
5. **Clean Up**: Use `setUp()` and `tearDown()` methods appropriately

### Test Data

1. **Use Fixtures**: Create test data in `setUp()` method
2. **Unique Data**: Ensure test data doesn't conflict between tests
3. **Realistic Data**: Use realistic test data that mirrors production scenarios

### Assertions

1. **Specific Assertions**: Use specific assertions (`assertEqual`, `assertIn`, etc.)
2. **Clear Messages**: Include descriptive error messages in assertions
3. **Multiple Checks**: Verify multiple aspects of responses when appropriate

### Running Tests

1. **Run Frequently**: Run tests after making changes
2. **Before Committing**: Always run tests before committing code
3. **In CI/CD**: Integrate tests into continuous integration pipeline

## Troubleshooting

### Common Issues

1. **Database Errors**: Ensure migrations are up to date
2. **Import Errors**: Check that all required modules are imported
3. **Authentication Issues**: Verify user setup in `setUp()` method
4. **URL Reverse Errors**: Check that URL names match in `urls.py`

### Debugging Tests

1. **Use `-v 2`**: Run tests with verbose output to see detailed information
2. **Print Statements**: Add temporary print statements to debug issues
3. **Test Database**: Use `--keepdb` to inspect test database after tests
4. **Isolate Tests**: Run individual tests to isolate problems

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

---

**Last Updated**: 2024
**Project**: advanced-api-project
**Test File**: `/api/test_views.py`
**Total Tests**: 26

