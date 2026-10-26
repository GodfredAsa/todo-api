OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Todo API",
        "description": (
            "API for registering users, authenticating, and managing their tasks."
        ),
        "version": "1.0.0",
    },
    "servers": [{"url": "/"}],
    "tags": [
        {"name": "Health"},
        {"name": "Authentication"},
        {"name": "Users"},
        {"name": "Tasks"},
    ],
    "paths": {
        "/api/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Check API health",
                "security": [],
                "responses": {
                    "200": {
                        "description": "The API is running.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"},
                                "example": {
                                    "status": 200,
                                    "message": "Application is up",
                                    "data": "Server is healthy",
                                },
                            }
                        },
                    }
                },
            }
        },
        "/api/v1/register": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Register a user",
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/RegistrationRequest"
                            },
                            "example": {
                                "preferred_name": "Alex",
                                "password": "example-password",
                            },
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "User registered.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"},
                                "example": {
                                    "status": 201,
                                    "message": "Registration successful",
                                    "data": {
                                        "user_id": "user-uuid",
                                        "preferred_name": "Alex",
                                    },
                                },
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                    "409": {"$ref": "#/components/responses/Conflict"},
                },
            }
        },
        "/api/v1/auth/login": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Authenticate and obtain an access token",
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginRequest"},
                            "example": {
                                "preferred_name": "Alex",
                                "password": "example-password",
                            },
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Login successful.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"},
                                "example": {
                                    "status": 200,
                                    "message": "Login successful",
                                    "data": "<access-token>",
                                },
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                },
            }
        },
        "/api/v1/tasks": {
            "post": {
                "tags": ["Tasks"],
                "summary": "Create a task",
                "security": [{"bearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CreateTaskRequest"
                            },
                            "example": {
                                "user_id": "user-uuid",
                                "name": "Finish API documentation",
                                "description": "Add OpenAPI documentation",
                                "priority": "medium",
                                "status": "pending",
                            },
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Task created.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"},
                                "example": {
                                    "status": 201,
                                    "message": "Task created successfully",
                                    "data": {
                                        "task_id": "task-uuid",
                                        "user_id": "user-uuid",
                                        "name": "Finish API documentation",
                                        "description": "Add OpenAPI documentation",
                                        "priority": "medium",
                                        "status": "pending",
                                        "created_at": "26/10/2026",
                                        "user": {
                                            "user_id": "user-uuid",
                                            "preferred_name": "Alex",
                                        },
                                    },
                                },
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            }
        },
        "/api/v1/tasks/search": {
            "get": {
                "tags": ["Tasks"],
                "summary": "Search a user's tasks",
                "description": (
                    "Filter a user's tasks by status, task name, and priority. "
                    "Name matching is case-insensitive and supports partial matches."
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {
                        "name": "status",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": [
                                "pending",
                                "in_progress",
                                "completed",
                                "cancelled",
                            ],
                        },
                    },
                    {
                        "name": "name",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "string"},
                    },
                    {
                        "name": "priority",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "urgent"],
                        },
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Matching tasks. Returns an array of task objects.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Task"},
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                    "500": {"$ref": "#/components/responses/InternalServerError"},
                },
            }
        },
        "/api/v1/users/{user_id}/tasks": {
            "get": {
                "tags": ["Users", "Tasks"],
                "summary": "List a user's tasks",
                "security": [{"bearerAuth": []}],
                "parameters": [{"$ref": "#/components/parameters/UserId"}],
                "responses": {
                    "200": {
                        "description": "Tasks belonging to the user.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Task"},
                                }
                            }
                        },
                    },
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            }
        },
        "/api/v1/users/{user_id}/tasks/{task_id}": {
            "parameters": [
                {"$ref": "#/components/parameters/UserId"},
                {"$ref": "#/components/parameters/TaskId"},
            ],
            "get": {
                "tags": ["Tasks"],
                "summary": "Get a user's task",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Task retrieved.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"}
                            }
                        },
                    },
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            },
            "put": {
                "tags": ["Tasks"],
                "summary": "Update a user's task",
                "security": [{"bearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/UpdateTaskRequest"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Task updated.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/BadRequest"},
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            },
            "delete": {
                "tags": ["Tasks"],
                "summary": "Delete a user's task",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Task deleted.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiResponse"},
                                "example": {
                                    "status": 200,
                                    "message": "User task deleted successfully",
                                    "data": None,
                                },
                            }
                        },
                    },
                    "401": {"$ref": "#/components/responses/Unauthorized"},
                    "404": {"$ref": "#/components/responses/NotFound"},
                },
            },
        },
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        },
        "parameters": {
            "UserId": {
                "name": "user_id",
                "in": "path",
                "required": True,
                "description": "UUID of the user.",
                "schema": {"type": "string"},
            },
            "TaskId": {
                "name": "task_id",
                "in": "path",
                "required": True,
                "description": "UUID of the task.",
                "schema": {"type": "string"},
            },
        },
        "schemas": {
            "ApiResponse": {
                "type": "object",
                "required": ["status", "message", "data"],
                "properties": {
                    "status": {"type": "integer", "example": 200},
                    "message": {"type": "string"},
                    "data": {
                        "nullable": True,
                        "description": "Response payload, null when there is no payload.",
                    },
                },
            },
            "ErrorResponse": {
                "type": "object",
                "required": ["status", "message", "data"],
                "properties": {
                    "status": {"type": "integer"},
                    "message": {"type": "string"},
                    "data": {"nullable": True},
                },
            },
            "RegistrationRequest": {
                "type": "object",
                "required": ["preferred_name", "password"],
                "properties": {
                    "preferred_name": {"type": "string"},
                    "password": {"type": "string", "format": "password"},
                },
            },
            "LoginRequest": {
                "type": "object",
                "required": ["preferred_name", "password"],
                "properties": {
                    "preferred_name": {"type": "string"},
                    "password": {"type": "string", "format": "password"},
                },
            },
            "CreateTaskRequest": {
                "type": "object",
                "required": ["user_id", "name"],
                "properties": {
                    "user_id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string", "nullable": True},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "default": "medium",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "cancelled"],
                        "default": "pending",
                    },
                },
            },
            "UpdateTaskRequest": {
                "type": "object",
                "required": ["name", "priority", "status"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string", "nullable": True},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "cancelled"],
                    },
                },
            },
            "Task": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "user_id": {"type": "string"},
                    "name": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "cancelled"],
                    },
                    "description": {"type": "string", "nullable": True},
                    "created_at": {
                        "type": "string",
                        "description": "Date formatted as day/month/year.",
                    },
                    "user": {"$ref": "#/components/schemas/User"},
                },
            },
            "User": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "preferred_name": {"type": "string"},
                },
            },
        },
        "responses": {
            "BadRequest": {
                "description": "Invalid or incomplete request.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "status": 400,
                            "message": "name is required",
                            "data": None,
                        },
                    }
                },
            },
            "Unauthorized": {
                "description": "Missing or invalid authentication credentials.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "status": 401,
                            "message": "Missing Authorization Header",
                            "data": None,
                        },
                    }
                },
            },
            "NotFound": {
                "description": "The requested user or task was not found.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "status": 404,
                            "message": "User not found",
                            "data": None,
                        },
                    }
                },
            },
            "Conflict": {
                "description": "A user with the preferred name already exists.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "status": 409,
                            "message": "Preferred name already taken",
                            "data": None,
                        },
                    }
                },
            },
            "InternalServerError": {
                "description": "An unexpected server error occurred.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "status": 500,
                            "message": "Internal Server Error",
                            "data": None,
                        },
                    }
                },
            },
        },
    },
}
