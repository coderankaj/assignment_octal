# FastAPI + MongoDB Project Setup

This repository contains a FastAPI-based backend using MongoDB as the database and Poetry for dependency management.

## Author
**Assignment by Ankaj Gupta**

## Prerequisites
Ensure you have the following installed:
- **Python 3.13**
- **Poetry** (for dependency management) → [Installation Guide](https://python-poetry.org/docs/#installation)
- **MongoDB** (running locally or using a cloud instance like MongoDB Atlas)

## Clone the Repository
```bash
# Clone the repo from GitHub
git clone https://github.com/coderankaj/assignment_octal.git
cd assignment_octal
```

## Setup the Virtual Environment & Install Dependencies
```bash
# Install dependencies using Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Configure Environment Variables
Create a `.env` file in the root directory and add the necessary configurations:
```ini
FA_ENVIRONMENT="dev"
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=fastapi_db
SECRET_KEY=ankaj_gupta
ACCESS_TOKEN_EXPIRE_MINUTES=3600
```
Modify these values according to your setup.

## Run MongoDB Locally
If you have MongoDB installed locally, start the service:
```bash
mongod --dbpath /path/to/your/db
```
Alternatively, use Docker to spin up MongoDB:
```bash
docker run -d --name mongodb -p 27017:27017 -v mongo_data:/data/db mongo
```

## Running the FastAPI Server
```bash
uvicorn src.app.routes:app --host 0.0.0.0 --port 8000 --reload
```
The server will be accessible at:
```
http://127.0.0.1:8000
```

## API Documentation
FastAPI provides automatic API documentation:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure
```
assignment_octal/
├── .venv/
├── src/
│   ├── config.py
│   ├── __init__.py
│   ├── app/
│   │   ├── database.py
│   │   ├── routes.py
│   │   ├── settings.py
│   │   └── __init__.py
│   ├── product/
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── api/
│   │       ├── crud.py
│   ├── users/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── __init__.py
│   │   ├── dependencies/
│   │   │   ├── permissions.py
│   │   │   └── __pycache__/
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── token.py
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── password.py
```

Enjoy building with FastAPI and MongoDB! 🚀

