# Django Rest Framework Task and Product Management System

## 🚀 Project Overview

This is a Django Rest Framework (DRF) based Task and Product Management System with JWT authentication, role-based access, PostgreSQL, unit tests, and API documentation.

### **Key Features**

- JWT-based authentication (Register, Login, Logout, Token Refresh, Forgot password, Reset Password)
- Role-based access control (Admin & Normal Users)
- Task Management (CRUD with status & priority)
- Product Management (Admin-only CRUD for categories, subcategories, and products)
- PostgreSQL database support
- Soft/hard deletes, indexing, and audit fields (`created_by`, `updated_by`)
- Unit tests for authentication, CRUD operations, and token handling
- API documentation with OpenAPI (Swagger)
- Rate limiting for API security

## 🛠️ Project Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/ChintanZignuts/Task-and-Product-Management.git
cd Task-and-Product-Management
```

### **2. Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Ensure PostgreSQL is Installed and Running**

This project uses PostgreSQL as the database. Make sure PostgreSQL is installed and running before proceeding.

### **5. Create a `.env` File**

Create a `.env` file in the root directory and add the following environment variables:

```ini
SECRET_KEY=your_secret_key_here
APP_DEBUG=True
APP_DB_NAME=your_db_name
APP_DB_USER=your_db_user
APP_DB_PASSWORD=your_db_password
APP_DB_HOST=localhost
APP_DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = your_mailtrap_user
EMAIL_HOST_PASSWORD = your_mailtrap_password
EMAIL_PORT = your_mailtrap_port
```

### **6. Set Up the Database**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **7. Create a Superuser (optional for admin access)**

```bash
python manage.py createsuperuser
```

Follow the prompt to set up an admin account.

### **9. Run the Seeder**

```bash
python manage.py seed_admin
```

### **10. Run the Development Server**

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### **11. Run Tests**

To ensure everything is working correctly, run:

```bash
python manage.py test
```

## Running Tests with Coverage

To ensure your code is well-tested, you can check the test coverage using `coverage.py`. Follow these steps:

### 1. Install Coverage

If you haven't installed `coverage`, install it using pip:

```bash
pip install coverage
```

### 2. Run Tests with Coverage

To measure test coverage, run:

```bash
coverage run --source=task_product_manager manage.py test
```

### 3. Generate Coverage Report

After running the tests, generate a coverage report:

```bash
coverage report
```

## **2. Running with Docker (Recommended)**

This project supports Docker for easier setup and deployment.

#### **2.1 Ensure Docker & Docker Compose are Installed**

Ensure you have Docker and Docker Compose installed:

```bash
docker --version  # Check Docker version
docker-compose --version  # Check Docker Compose version
```

#### **2.2 Create an `.env` File**

Create a `.env` file in the root directory and add the following environment variables:

```ini
SECRET_KEY=your_secret_key_here
APP_DEBUG=True
APP_DB_NAME=task_db
APP_DB_USER=task_user
APP_DB_PASSWORD=your_db_password
APP_DB_HOST=postgres_db
APP_DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST='sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER=your_mailtrap_user
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_PORT=your_mailtrap_port
```

#### **2.3 Start the Containers**

Run the following command to build and start the Django and PostgreSQL containers:

```bash
docker-compose up -d --build
```

This will:

- Start the PostgreSQL database (`postgres_db` container)
- Start the Django application (`django_app` container)

#### **2.4 Apply Database Migrations**

Once the containers are up, run the migrations inside the Django container:

```bash
docker-compose exec django_app python manage.py migrate
```

#### **2.5 Create a Superuser (Admin Panel Access)**

```bash
docker-compose exec django_app python manage.py createsuperuser
```

#### **2.6 Run the Seeder**

```bash
docker-compose exec django_app python manage.py seed_admin
```

#### **2.7 Access the Application**

- API Base URL: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin/`
- Swagger API Docs: `http://127.0.0.1:8000/api/swagger/`

#### **2.8 Stopping the Containers**

To stop the running containers:

```bash
docker-compose down
```

#### **2.9 Restarting Containers**

To restart the containers without rebuilding:

```bash
docker-compose up -d
```

---

## Running Tests with Docker

Run tests inside the Docker container:

```bash
docker-compose exec web python manage.py test
```

To check test coverage:

```bash
docker-compose exec web coverage run --source=task_product_manager manage.py test
docker-compose exec web coverage report
```

## 📌 API Endpoints

### **Authentication**

| Method | Endpoint                                     | Description                   |
| ------ | -------------------------------------------- | ----------------------------- |
| POST   | `/api/auth/register/`                        | Register a new user           |
| POST   | `/api/auth/login/`                           | Login and get JWT tokens      |
| POST   | `/api/auth/refresh/`                         | Refresh JWT access token      |
| POST   | `/api/auth/logout/`                          | Logout user (blacklist token) |
| POST   | `/api/auth/forgot-password/`                 | Request password reset email  |
| POST   | `/api/auth/reset-password/{uidb64}/{token}/` | Reset user password           |

### **Task Management**

| Method | Endpoint           | Description                    |
| ------ | ------------------ | ------------------------------ |
| GET    | `/api/tasks/`      | List all tasks (user-specific) |
| POST   | `/api/tasks/`      | Create a new task              |
| GET    | `/api/tasks/{id}/` | Retrieve a task                |
| PUT    | `/api/tasks/{id}/` | Update a task                  |
| DELETE | `/api/tasks/{id}/` | Delete a task                  |

### **Category Management (Admin Only)**

| Method | Endpoint                        | Description                     |
| ------ | ------------------------------- | ------------------------------- |
| GET    | `/api/categories/`              | List all categories             |
| POST   | `/api/categories/`              | Create a new category           |
| GET    | `/api/categories/{id}/`         | Retrieve a category             |
| PUT    | `/api/categories/{id}/`         | Update a category               |
| DELETE | `/api/categories/{id}/delete/`  | Soft delete a category          |
| POST   | `/api/categories/{id}/restore/` | Restore a soft-deleted category |

### **Product Management (Admin Only)**

| Method | Endpoint                      | Description                    |
| ------ | ----------------------------- | ------------------------------ |
| GET    | `/api/products/`              | List all products              |
| POST   | `/api/products/`              | Create a new product           |
| GET    | `/api/products/{id}/`         | Retrieve a product             |
| PUT    | `/api/products/{id}/`         | Update a product               |
| DELETE | `/api/products/{id}/delete/`  | Soft delete a product          |
| POST   | `/api/products/{id}/restore/` | Restore a soft-deleted product |

For full API documentation, visit `http://127.0.0.1:8000/api/swagger/` (once the server is running).

| Documentation                   | URL                                |
| ------------------------------- | ---------------------------------- |
| Swagger UI (Interactive API)    | http://127.0.0.1:8000/api/swagger/ |
| ReDoc UI (Alternative API Docs) | http://127.0.0.1:8000/api/redoc/   |
| OpenAPI Schema (JSON)           | http://127.0.0.1:8000/api/schema/  |

## 🔗 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## 🛡️ Environment & Security Best Practices

- **Never commit the `.env` file** (add it to `.gitignore`).
- Use **strong passwords** for the admin account.
- Enable **HTTPS** in production.
- Set `DEBUG=False` before deploying to production.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
