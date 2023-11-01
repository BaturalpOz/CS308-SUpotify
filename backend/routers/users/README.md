# User Management API Documentation

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
  - [Create User](#create-user)
  - [Get User](#get-user)
  - [Update User](#update-user)
  - [Delete User](#delete-user)
  - [List All Users](#list-all-users)
  
## Overview

This API documentation provides detailed information about the endpoints available in our user management system.

## Endpoints

### Create User

**Endpoint:** `backend/routers/users`

**Method:** `POST`

**Description:** Creates a new user.

**Request Body:**
\```
{
  "username": "string",
  "email": "string",
  "password": "string"
}
\```

**Response:**
- **201 Created**: Successfully created a new user.
- **400 Bad Request**: Invalid input.

### Get User

**Endpoint:** `backend/routers/users/{userId}`

**Method:** `GET`

**Description:** Retrieves the details of a specific user.

**Path Parameters:**
- `userId`: The unique identifier of the user.

**Response:**
- **200 OK**: Successfully retrieved user details.
- **404 Not Found**: User does not exist.

### Update User

**Endpoint:** `backend/routers/users/{userId}`

**Method:** `PUT`

**Description:** Updates the details of a specific user.

**Path Parameters:**
- `userId`: The unique identifier of the user.

**Request Body:**
\```
{
  "username": "string",
  "email": "string"
}
\```

**Response:**
- **200 OK**: Successfully updated user details.
- **400 Bad Request**: Invalid input.
- **404 Not Found**: User does not exist.

### Delete User

**Endpoint:** `backend/routers/users/{userId}`

**Method:** `DELETE`

**Description:** Deletes a specific user.

**Path Parameters:**
- `userId`: The unique identifier of the user.

**Response:**
- **204 No Content**: Successfully deleted the user.
- **404 Not Found**: User does not exist.

### List All Users

**Endpoint:** `backend/routers/users`

**Method:** `GET`

**Description:** Retrieves a list of all users.

**Response:**
- **200 OK**: Successfully retrieved the list of users.