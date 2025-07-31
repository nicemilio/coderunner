# Code Racer - Setup Guide

This document outlines the steps to set up the Code Racer project for development.

## 1. System Dependencies (Apt Packages)

Before installing Python dependencies, ensure you have the following system packages installed. These are typically needed for PostgreSQL client libraries, compilation tools, or other core utilities.

**For Debian/Ubuntu-based systems:**

```bash
sudo apt update
sudo apt install -y postgresql build-essential libpq-dev python3-dev
```
## 2. Python Environment Setup

```bash
python3 -m venv CodeRunnerVenv

# Activate the virtual environment
source CodeRunnerVenv/bin/activate # On Linux/macOS

# Install Python dependencies
pip install -r requirements.txt
```

## 3. Postgresql Setup

Make sure your  Postgresql databse is running, if not, start it by running:
```bash
systemctl start postgresql
```

Create a user account by following these steps:
```bash
# Switch to the postgres user
sudo -i -u postgres
```
Run the following SQL Commands:
```SQL
// Creating an user account and assigning privileges
CREATE USER YourUsername WITH PASSWORD 'YourPassword';
CREATE DATABASE coderunner OWNER YourUsername;
GRANT ALL PRIVILEGES ON DATABASE coderunner TO YourUsername;
```

## 4. Setup .env file

In the root directory of the project, create a .env file containing the following string
```
DATABASE_URL=postgresql://YourUsername:YourPassword@localhost:5432/coderunner
```

## 5. Apply the lastest database migration

We use Alembic for database migrations, so run:
```bash
alembic upgrade head
```
