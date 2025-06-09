# LockLink - A Secure URL Shortener (Tugas Kriptografi)

LockLink is a demo Django-based URL shortener project that provides secure, encrypted, and optionally password-protected short links.

## Features

-   **URL Shortening**: Converts long URLs into a manageable short code.
-   **URL Encryption**: All original URLs are encrypted at rest in the database, ensuring that even with database access, the original links remain private.
-   **Password Protection**: Optionally protect links with a password for an added layer of security.
-   **Link Expiration**: Set an expiration time (in minutes) for any short link.

## Deployment Guide

This guide will walk you through setting up the project for local development.

### 1. Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)
-   Git

### 2. Setup Instructions

**Step 1: Clone the Repository**
```bash
# Replace <your-repository-url> with the actual URL of the repository
git clone <your-repository-url>
cd Locklink
```

**Step 2: Create and Activate a Virtual Environment**
It's a strong convention and best practice to use a virtual environment to isolate project dependencies.

*For Windows:*
```bash
python -m venv venv
venv\\Scripts\\activate
```

*For macOS/Linux:*
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
Install all required packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

**Step 4: Create the Environment File (`.env`)**
The project uses a `.env` file to manage sensitive configuration. Create a file named `.env` in the project root directory. You will need to generate values for the following keys:

-   `SECRET_KEY`: A secret key for this specific Django installation. Used for cryptographic signing.
-   `FERNET_KEY`: The symmetric encryption key used to encrypt and decrypt URLs.

You can generate these keys from your terminal (make sure your virtual environment is activated):

1.  **Generate `SECRET_KEY`**:
    ```bash
    python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

2.  **Generate `FERNET_KEY`**:
    ```bash
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```

Copy the generated values into your `.env` file. It should look like this:
```
SECRET_KEY='your-generated-django-secret-key'
FERNET_KEY='your-generated-fernet-key'
```

**Step 5: Run Database Migrations**
This command applies the database schema and any subsequent changes to your database.
```bash
python manage.py migrate
```

**Step 6: Run the Development Server**
You can now start the Django development server.
```bash
python manage.py runserver
```
The application will be running at `http://127.0.0.1:8000/`.

### Production Deployment Notes

For a live production environment, please ensure you:
-   Set `DEBUG=False` in your configuration (e.g., by adding `DEBUG=False` to your `.env` file).