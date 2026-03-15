# FastAPI Backend

A minimal FastAPI backend application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Direct execution
```bash
python main.py
```

### Method 2: Using uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /` - Returns `{"status": "running"}`
