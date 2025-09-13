from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer
from typing import Optional
from datetime import timedelta
from app import crud
from app.models import Employee, UpdateEmployee, UserLogin, Token, User, UserCreate
from app.utils import get_collection_indexes, get_index_stats
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_user, security



router = APIRouter()

# auth endpoints
@router.post("/register", response_model=User)
def register_user(user_data: UserCreate):
    """register new user"""
    # check if username taken
    new_user = create_user(user_data)
    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    # return user without password
    return User(
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        disabled=new_user.disabled
    )

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: UserLogin):
    """login to get token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """get current user info"""
    return current_user

# Protected employee endpoints
@router.post("/employees")
def create_employee(emp: Employee, current_user: User = Depends(get_current_user)):
    try:
        # check if employee already exists
        existing_emp = crud.get_employee(emp.employee_id)
        if existing_emp:
            raise HTTPException(status_code=400, detail="Employee already exists with this ID")
        
        # convert to dict and handle datetime
        employee_data = emp.dict()
        
        # convert joining_date string to datetime if needed
        if isinstance(employee_data.get('joining_date'), str):
            from datetime import datetime
            employee_data['joining_date'] = datetime.fromisoformat(employee_data['joining_date'])
        
        result = crud.create_employee(employee_data)
        return {"status": "ok", "id": emp.employee_id}
    except Exception as e:
        print(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@router.get("/employees")
def get_employees(
    department: Optional[str] = None,
    page:  int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    skip_count =   (page - 1) * limit

    if department:
        employees=  list(crud.list_by_department(department,skip_count, limit))
        total_count= crud.count_by_department(department)
    else:
        employees =   list(crud.list_all(skip_count,limit))
        total_count  = crud.count_all()

    
    for emp in employees:
        emp["_id"]= str(emp["_id"])  

    total_pages = (total_count + limit - 1) // limit
    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "pages": total_pages,
        "results": employees,
    }


@router.get("/employees/avg-salary")
def avg_salary(current_user: User = Depends(get_current_user)):
    res = crud.avg_salary_by_department()
    data= []
    for r in res:
        data.append({"dept": r["_id"], "avg": r["avg_salary"]})
    return data


@router.get("/employees/search")
def search_employees(skill: str, current_user: User = Depends(get_current_user)):
    results = list(crud.search_by_skill(skill))
    for r in results:
        r["_id"]= str(r["_id"])
    return results


@router.get("/employees/{employee_id}")
def get_employee(employee_id: str, current_user: User = Depends(get_current_user)):
    emp = crud.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")
    emp["_id"]= str(emp["_id"])
    return emp


@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, emp: UpdateEmployee, current_user: User = Depends(get_current_user)):
    update_data= emp.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    
    crud.update_employee(employee_id, update_data)
    return {"updated": True, "employee_id": employee_id}


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, current_user: User = Depends(get_current_user)):
    deleted= crud.delete_employee(employee_id)
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"deleted": True}


# admin endpoints for checking database indexes
@router.get("/admin/indexes")
def get_indexes():
    """Show all indexes"""
    indexes = get_collection_indexes()
    return {"indexes": indexes}


@router.get("/admin/index-stats")
def get_index_statistics():
    """Show index usage stats"""
    stats= get_index_stats()
    return {"index_stats": stats}
