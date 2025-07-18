# Thuriyam Base API - Postman Collection

This Postman collection provides comprehensive coverage of all available endpoints in the Thuriyam Base FastAPI microservice template.

## Collection Overview

The collection is organized into five main sections:

1. **Health Check** - Basic service health verification
2. **Authentication** - User registration and login endpoints
3. **Users** - User management endpoints (CRUD operations)
4. **Todos** - Todo management endpoints (CRUD operations with filtering)
5. **Campaigns** - Campaign management endpoints (CRUD operations with advanced filtering)

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
- **`campaign_id`**: ID of a specific campaign for testing individual campaign operations

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
   - Body: Form data with username, password, and optional scopes (space-separated)
   - **Recommended scopes**: `me campaigns:read campaigns:write campaigns:manage`
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

### Step 5: Campaign Management (Authenticated)
The campaign endpoints require authentication with appropriate campaign scopes and provide comprehensive campaign management:
- **Create Campaign**: `POST /api/v1/campaigns/`
- **Get All Campaigns**: `GET /api/v1/campaigns/` (with filtering options)
- **Get Campaigns by Status**: `GET /api/v1/campaigns/?status=active`
- **Get Campaigns by Type**: `GET /api/v1/campaigns/?campaign_type=social`
- **Search Campaigns by Name**: `GET /api/v1/campaigns/?name=Summer`
- **Get Active Campaigns Only**: `GET /api/v1/campaigns/?active_only=true`
- **Get Campaigns by Date Range**: `GET /api/v1/campaigns/date-range/?start_date=...&end_date=...`
- **Get Campaign by ID**: `GET /api/v1/campaigns/{campaign_id}`
- **Update Campaign**: `PUT /api/v1/campaigns/{campaign_id}`
- **Update Campaign Status**: `PATCH /api/v1/campaigns/{campaign_id}/status?new_status=active`
- **Toggle Campaign Active Status**: `PATCH /api/v1/campaigns/{campaign_id}/toggle-active`
- **Delete Campaign**: `DELETE /api/v1/campaigns/{campaign_id}`

## Authentication Scopes

The API uses OAuth2 scopes for authorization:

### User Management Scopes
- **`me`**: Access to own user profile
- **`users`**: Access to list all users
- **`admin`**: Full administrative access

### Campaign Management Scopes
- **`campaigns:read`**: Read campaign information
- **`campaigns:write`**: Create and update campaigns  
- **`campaigns:manage`**: Full campaign management including status changes and deletion

### Scope Usage by Endpoint
- **Campaign Read Operations**: Require `campaigns:read` scope
- **Campaign Create/Update**: Require `campaigns:write` scope
- **Campaign Status Management/Delete**: Require `campaigns:manage` scope

## Todo Filtering Options

The todo endpoints support several filtering options:

- **Pagination**: Use `skip` and `limit` parameters
- **Completion Status**: Filter by `completed=true` or `completed=false`
- **Title Search**: Search by title containing text using `title` parameter

## Campaign Filtering Options

The campaign endpoints provide extensive filtering capabilities:

- **Pagination**: Use `skip` and `limit` parameters for all endpoints
- **Status Filtering**: Filter by `status` (draft, active, paused, completed, cancelled)
- **Type Filtering**: Filter by `campaign_type` (email, social, display, search, content, influencer, other)
- **Name Search**: Search by campaign name containing text using `name` parameter
- **Active Only**: Use `active_only=true` to get only campaigns with status='active' and is_active=true
- **Date Range**: Use `/date-range/` endpoint with `start_date` and `end_date` parameters (ISO 8601 format)

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

username=johndoe&password=securepassword123&scope=me campaigns:read campaigns:write campaigns:manage
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

### Create a Campaign
```json
POST /api/v1/campaigns/
Authorization: Bearer {access_token}
{
  "name": "Summer Marketing Campaign",
  "description": "Comprehensive summer marketing campaign targeting millennials",
  "campaign_type": "social",
  "status": "draft",
  "start_date": "2024-06-01T00:00:00Z",
  "end_date": "2024-08-31T23:59:59Z",
  "budget": 50000.00,
  "target_audience": "Millennials aged 25-35, interested in outdoor activities",
  "is_active": true
}
```

### Get Campaigns with Filtering
```
GET /api/v1/campaigns/?status=active&campaign_type=social&skip=0&limit=10
Authorization: Bearer {access_token}
```

### Get Campaigns by Date Range
```
GET /api/v1/campaigns/date-range/?start_date=2024-06-01T00:00:00Z&end_date=2024-12-31T23:59:59Z&skip=0&limit=100
Authorization: Bearer {access_token}
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
3. **Request Appropriate Scopes**: When logging in, request all needed scopes (`me campaigns:read campaigns:write campaigns:manage`)
4. **Use Variables**: Set the `access_token` variable after login to automatically use it in subsequent requests
5. **Test Todo Operations**: Use the todo endpoints to test CRUD operations without authentication
6. **Test Campaign Operations**: Use the campaign endpoints to test advanced CRUD operations with authentication
7. **Check Response Status**: Verify that responses match expected status codes (401 for missing auth, 403 for insufficient scopes)
8. **Use Filtering**: Test the various filtering options available for todo and campaign endpoints
9. **Test Date Ranges**: Use campaign date range filtering to test date-based queries
10. **Test Status Management**: Use campaign status update and toggle operations
11. **Verify Authorization**: Test accessing endpoints without proper scopes to verify security

## Troubleshooting

- **Connection Refused**: Ensure the API server is running on the correct port
- **401 Unauthorized**: Check that the access token is valid and not expired
- **403 Forbidden**: Verify that your token has the required scope for the endpoint
  - For campaigns: Ensure you have `campaigns:read`, `campaigns:write`, or `campaigns:manage` as needed
  - Check the scope requirements in the documentation above
- **404 Not Found**: Check that the resource ID exists in the database
- **422 Validation Error**: Check request body format and required fields

## Database Setup

Before testing, ensure the database is initialized:

```bash
# From the app directory
cd app
python ../scripts/init_db.py
```

This will create the SQLite database with all necessary tables. 