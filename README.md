# Task Management API

## Overview
This project is a **Task Management API** built using **Django REST Framework**. It provides endpoints to manage tasks, including creating, updating, deleting, and viewing tasks. The API supports user authentication and task assignments to users.

The key features include:
- User registration and authentication.
- CRUD operations on tasks.
- Task assignment to users.
- Filtering tasks by status, due date, etc.

## Installation and Setup

### Prerequisites
- Python 3.x
- Django 3.x+
- Django REST Framework
- Virtual Environment (Optional, but recommended)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/UnknownLoop11/Task-Management-API.git
   cd Task-Management-API
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin) (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints and Sample Requests

### Authentication
- **POST** `/api/auth/login/`
  - Request body:
    ```json
    {
      "username": "exampleuser",
      "password": "password123"
    }
    ```
  - Response:
    ```json
    {
      "access": "your_jwt_token",
      "refresh": "your_refresh_token"
    }
    ```

- **POST** `/api/auth/register/`
  - Request body:
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "newpassword"
    }
    ```

### Tasks
- **GET** `/api/tasks/` - Retrieve all tasks (requires authentication)
  - **(Optional) Parameters for Filtering:**
    - **status** - [ 'pending', 'in_progress', 'completed' ]
    - **priority** - [ 'low', 'medium', 'high' ]
    - **sort_by** - [ 'created_at', 'due_date' ]
  - Response:
    ```json
    [
      {
        "id": 1,
        "title": "Finish the project",
        "description": "Complete the API development by the end of the week",
        "status": "Pending",
        "due_date": "2024-10-20",
        "created_at": "2024-10-14T09:24:47.602577Z",
        "user": 1
      }
    ]
    ```

- **POST** `/api/tasks/` - Create a new task (requires authentication)
  - Request body:
    ```json
    {
      "title": "Complete unit testing",
      "description": "Ensure all test cases pass for task management", // Optional
      "status": "pending", // ['pending', 'in_progress', 'completed']
      "priority": "low", // ['low', 'medium', 'high']
      "due_date": "2024-10-18" // YYYY-mm-dd
    }
    ```
  - Response:
    ```json
    {
      "id": 2,
      "title": "Complete unit testing",
      "description": "Ensure all test cases pass for task management",
      "status": "In Progress",
      "due_date": "2024-10-18"
      "created_at": "2024-10-14T09:24:47.602577Z",
      "user": 1
    }
    ```

- **GET** `/api/tasks/<id>/` - Get task detail
  - Request body:
    ```json
    {
      "id": 2,
      "title": "Complete unit testing",
      "description": "Ensure all test cases pass for task management",
      "status": "In Progress",
      "due_date": "2024-10-18"
      "created_at": "2024-10-14T09:24:47.602577Z",
      "user": 1
    }
    ```

- **PUT** `/api/tasks/<id>/` - Update an existing task
  - Request body:
    ```json
    {
      "title": "Update unit tests",
      "status": "Completed"
    }
    ```

- **DELETE** `/api/tasks/<id>/` - Delete a task

## Tests

Run the tests using:
```bash
python manage.py test
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This file assumes a standard Django REST API setup with common endpoints for authentication and task management. You can update it based on the specific functionality provided in your project and the details in your GitHub repository. Let me know if you need further customization!
