# Planetarium API 🪐

This is a RESTful API service for managing a planetarium, built with Django REST Framework. It provides functionality for managing astronomy shows, show sessions, user reservations, and more. The project is containerized with Docker for easy setup and deployment.

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Django](https://img.shields.io/badge/django-5.2-green.svg)
![Django REST Framework](https://img.shields.io/badge/DRF-3.15-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg?logo=docker)

---

## ✨ Features

- ✅ **Token-based Authentication** for secure API access.
- ✅ **User Management** including registration and personal profile management.
- ✅ **Full CRUD Functionality** for core models like Show Sessions.
- ✅ **Admin Panel** at `/admin/` for easy data management.
- ✅ **Interactive API Documentation** with Swagger UI and ReDoc.
- ✅ **Advanced Filtering** for shows and sessions.
- ✅ **Image Uploads** for astronomy show posters.
- ✅ **Containerized with Docker** for consistent and reproducible environments.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Authentication:** DRF Token Authentication
- **API Documentation:** drf-spectacular (Swagger/ReDoc)

---

## 🚀 Getting Started with Docker

This project is fully containerized, so all you need is Docker and Docker Compose.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/olegicks/planetarium_api.git
    cd planetarium_api
    ```

2.  **Create your environment file:**
    Create a `.env` file by copying the `env.example` template. This file will hold your secret keys and configuration.
    ```bash
    cp env.example .env
    ```
    *If `env.example` doesn't exist, create `.env` with this content:*
    ```ini
    # .env
    SECRET_KEY=your-super-secret-key-that-is-very-long-and-secure
    DEBUG=1

    # Postgres settings for Docker
    POSTGRES_DB=planetarium_db
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ```

3.  **Build and run the containers:**
    This command will build the necessary Docker images and start the application and database services in the background.
    ```bash
    docker-compose build
    docker-compose up -d
    ```

4.  **Apply database migrations:**
    This crucial step initializes the database schema inside the running container.
    ```bash
    docker-compose exec planetarium python manage.py migrate
    ```

5.  **Done!** The API is now running and available at `http://localhost:8000`.

6.  **(Optional) To stop and remove all containers:**
    ```bash
    docker-compose down
    ```
---

## 🔑 API Authentication

Access to protected endpoints requires an authentication token.

1.  **Register a User:**
    Send a `POST` request to `http://localhost:8000/user/create/` with your `email` and `password`.

2.  **Login and Get a Token:**
    Send a `POST` request to `http://localhost:8000/user/login/` with the `email` and `password` you just registered. The response will contain your authentication `token`.

3.  **Authenticate Your Requests:**
    To access protected endpoints, include the `Authorization` header in your requests. **Note the "Token" prefix.**
    ```
    Authorization: Token <your_token>
    ```

---

## 📖 API Endpoints

### User Management & Documentation

| Endpoint | Supported Methods | Description |
| :--- | :--- | :--- |
| `/user/create/` | `POST` | Register a new user. |
| `/user/login/` | `POST` | Login to get an auth token. |
| `/user/me/` | `GET`, `PUT`, `PATCH` | Retrieve or update your profile. |
| `/api/doc/swagger/`| `GET` | View interactive API documentation. |
| `/api/doc/redoc/` | `GET` | View alternative API documentation. |

### Planetarium Core API (`/api/`)

| Resource | URL | Supported Methods |
| :--- | :--- | :--- |
| **Show Themes** | `/api/show_themes/` | `GET`, `POST` |
| **Astronomy Shows**| `/api/astronomy_shows/` | `GET`, `POST` |
| | `/api/astronomy_shows/{id}/` | `GET` |
| | `/api/astronomy_shows/{id}/upload-image/`| `POST` |
| **Planetarium Domes**| `/api/planetarium_domes/` | `GET`, `POST` |
| **Show Sessions** | `/api/show_sessions/` | `GET`, `POST` |
| | `/api/show_sessions/{id}/` | `GET`, `PUT`, `PATCH`, `DELETE`|
| **Reservations** | `/api/reservations/` | `GET`, `POST` |