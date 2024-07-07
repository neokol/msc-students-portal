# Backend - Student Grades Portal

This is the backend service for the Student Grades Portal application. It is built with FastAPI and uses PostgreSQL as its database.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)

## Requirements

- Python 3.11
- PostgreSQL
- Docker (for deployment)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/student-grades-portal.git
   cd student-grades-portal/backend
   ```

2. Create a virtual environment and activate it

```bash
python3.11 -m venv venv
source venv/bin/activate
```

For windows users user:

```bash
.\.venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Environment Variables

Create a .env file in the backend directory and add the following environment variables

Replace username, password, and your_secret_key with your actual database username, password, and a secret key for JWT.

5. Running the Application

nsure PostgreSQL is running and the database is created.

Run the application:

```bash
uvicorn app.main:app --reload
```

The backend service will be available at http://localhost:8000/docs
