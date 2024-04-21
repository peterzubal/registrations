
# Student Management System API

## Overview
This Django-based REST API manages student user accounts and provides endpoints for registration, login, logout, and profile updates. It utilizes the Django REST Framework for building RESTful APIs and supports token-based authentication.

## Features
- **User Registration**: Register a new student account.
- **User Login**: Login to an existing student account and receive an authentication token.
- **User Logout**: Logout from the application and invalidate the session token.
- **Update Profile**: Update student user profile details.

## Installation

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher
- Django REST Framework

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory and install dependencies:
   ```bash
   cd <project-directory>
   pip install -r requirements.txt
   ```
3. Run migrations to set up the database:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Start testing the API using a REST client like Postman.
6. run the following command to create a superuser
   ```bash
   python manage.py createsuperuser
   ```
7. run the following command to test the API
   ```bash
   python manage.py test
   ```
   

## API Endpoints

- **Register**:
  - `POST /api/register/`
  - Payload: `{"username": "user", "password": "pass", "full_name": "Full Name", "address": "Address", "date_of_birth": "YYYY-MM-DD", "phone_number": "Phone", "disabilities": "None"}`
- **Login**:
  - `POST /api/login/`
  - Payload: `{"username": "user", "password": "pass"}`
- **Logout**:
  - `POST /api/logout/`
- **Update Profile**:
  - `POST /api/update_profile/`
  - Payload: `{"full_name": "New Name", "address": "New Address", ...}`

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
