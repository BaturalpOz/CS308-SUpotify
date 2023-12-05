# Backend

This is the backend for a music streaming application. It is built with Flask and uses Firebase for database operations.

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3
- pip (Python package manager)
- Git (Version control system)

### Setup Instructions

### 1. Virtual Environment

#### For Mac/Linux

```bash

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

```

#### For Windows
    
```bash

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

```

### 2. Install Dependencies

```bash

# Install dependencies
pip install -r requirements.txt

```

### 4. Environment Variables

Create a .env file and add the following environment variables:

```bash
FLASK_APP=run.py
FLASK_ENV=development
FIREBASE_ADMINSDK_JSON_PATH=firebase-adminsdk.json
```

### 5. Run the Application

```bash

flask run

```

### 6. Deactivate the Virtual Environment

```bash

deactivate

```