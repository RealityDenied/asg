# Employee Management API

A FastAPI-based employee management app with JWT authentication & MongoDB storage.

## Personal Details
- Name - Vikash Kumar
- Email - vikashkumar3791kzq<@>gmail.com
- Roll no - 2022UGPI010
- Institute - National Institute of Technology Jamshedpur


## Tasks Done
- All 3 sections Completed (All 7 CRUD APIs completed)
- All 4 bonuses challenges completed ->
- Implemented pagination for employee listing. 
- Added MongoDB index on employee_id. 
- Implement schema validation (e.g., using MongoDB JSON Schema). 
- Add JWT authentication for protected routes. ( Login and Signup with password hashing as well )


### Prerequisites
- Python 3.8+
- MongoDB running on localhost:27017

### Installation

1. Clone the repo and navigate to project folder
```bash
git clone <repo-url>
cd asg
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate.ps1  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the server
```bash
uvicorn app.main:app --reload
```

Server starts at `http://127.0.0.1:8000`

## API Usage

### Authentication

**Register a new user:**
```bash
POST /register
{
  "username": "john_doe",
  "password": "password123",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

**Login to get JWT token:**
```bash
POST /login
{
  "username": "john_doe", 
  "password": "password123"
}
```

**Use token in Swagger UI:**
1. Go to `http://127.0.0.1:8000/docs`
2. Click "Authorize" button
3. Enter: `YOUR_JWT_TOKEN`

### Employee Operations

**Create employee:**
```bash
POST /employees
{
  "employee_id": "E001",
  "name": "Jane Smith",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "FastAPI", "MongoDB"]
}

-- You can explore all other features in swagger UI docs as well similarly.
```

Mock accounts for testing:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`


---

Built with FastAPI, MongoDB, and JWT authentication.
