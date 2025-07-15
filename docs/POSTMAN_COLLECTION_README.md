# Thuriyam Base API - Postman Collection

This Postman collection provides comprehensive coverage of all available endpoints in the Thuriyam Base FastAPI microservice template.

## Collection Overview

The collection is organized into four main sections:

1. **Health Check** - Basic service health verification
2. **Authentication** - User registration and login endpoints
3. **Users** - User management endpoints (CRUD operations)
4. **Todos** - Todo management endpoints (CRUD operations with filtering)

## Setup Instructions

### 1. Import the Collection

1. Open Postman
2. Click "Import" button
3. Select the `thuriyam-base-api.postman_collection.json` file
4. The collection will be imported with all endpoints

### 2. Configure Environment Variables

The collection uses the following variables that you can configure:

- **`base_url`**: The base URL of your API server (default: `http://localhost:8000`)
- **`access_token`**: JWT access token for authenticated requests (will be set after login)
- **`todo_id`**: ID of a specific todo for testing individual todo operations

### 3. Start the API Server

Before testing the endpoints, make sure your API server is running:

```bash
# From the app directory
cd app
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

## Usage Workflow

### Step 1: Health Check
Start by testing the health check endpoint to ensure the server is running:
- **Health Check**: `GET /`

### Step 2: Authentication
1. **Create User**: Register a new user account
   - Method: `POST /api/v1/users/`
   - Body: JSON with username, email, full_name, and password

2. **Login for Access Token**: Get an access token for authenticated requests
   - Method: `POST /api/v1/users/token`
   - Body: Form data with username, password, and optional scope
   - **Important**: Copy the `access_token` from the response and set it as the `access_token` variable

### Step 3: User Management (Authenticated)
Once you have an access token, you can test user management endpoints:
- **Get Current User**: `GET /api/v1/users/me` (requires 'me' scope)
- **Get All Users**: `GET /api/v1/users/` (requires 'users' scope)
- **Get User by Username**: `GET /api/v1/users/{username}` (requires 'admin' scope)
- **Update User**: `PUT /api/v1/users/{username}` (requires 'admin' scope)
- **Delete User**: `DELETE /api/v1/users/{username}` (requires 'admin' scope)

### Step 4: Todo Management
The todo endpoints don't require authentication and can be tested directly:
- **Create Todo**: `POST /api/v1/todos/`
- **Get All Todos**: `GET /api/v1/todos/` (with optional filtering)
- **Get Todo by ID**: `GET /api/v1/todos/{todo_id}`
- **Update Todo**: `PUT /api/v1/todos/{todo_id}`
- **Toggle Todo**: `PATCH /api/v1/todos/{todo_id}/toggle`
- **Delete Todo**: `DELETE /api/v1/todos/{todo_id}`

## Authentication Scopes

The API uses OAuth2 scopes for authorization:

- **`me`**: Access to own user profile
- **`users`**: Access to list all users
- **`admin`**: Full administrative access

## Todo Filtering Options

The todo endpoints support several filtering options:

- **Pagination**: Use `skip` and `limit` parameters
- **Completion Status**: Filter by `completed=true` or `completed=false`
- **Title Search**: Search by title containing text using `title` parameter

## Example Requests

### Create a User
```json
POST /api/v1/users/
{
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```

### Login
```
POST /api/v1/users/token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepassword123&scope=me
```

### Create a Todo
```json
POST /api/v1/todos/
{
  "title": "Complete API documentation",
  "description": "Create comprehensive API documentation for the project",
  "completed": false
}
```

### Get Todos with Filtering
```
GET /api/v1/todos/?completed=false&skip=0&limit=10&title=API
```

## Error Handling

The collection includes proper error handling for common scenarios:
- 401 Unauthorized: Invalid or missing authentication
- 403 Forbidden: Insufficient permissions for the requested scope
- 404 Not Found: Resource not found
- 422 Validation Error: Invalid request data

## Tips for Testing

1. **Start with Health Check**: Always verify the server is running first
2. **Follow the Authentication Flow**: Create a user, then login to get an access token
3. **Use Variables**: Set the `access_token` variable after login to automatically use it in subsequent requests
4. **Test Todo Operations**: Use the todo endpoints to test CRUD operations without authentication
5. **Check Response Status**: Verify that responses match expected status codes
6. **Use Filtering**: Test the various filtering options available for todo endpoints

## Troubleshooting

- **Connection Refused**: Ensure the API server is running on the correct port
- **401 Unauthorized**: Check that the access token is valid and not expired
- **403 Forbidden**: Verify that your token has the required scope for the endpoint
- **404 Not Found**: Check that the resource ID exists in the database

## Database Setup

Before testing, ensure the database is initialized:

```bash
# From the app directory
cd app
python ../scripts/init_db.py
```

This will create the SQLite database with all necessary tables. 