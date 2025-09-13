from fastapi import APIRouter, HTTPException
from typing import Optional
from app import crud
from app.models import Employee, UpdateEmployee

router = APIRouter()

@router.post("/employees")
def create_employee(emp: Employee):
    # check duplicate
    existing = crud.get_employee(emp.employee_id)
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists with this ID")
    
    crud.create_employee(emp.dict())  # using dict() instead of model_dump()
    return {"status": "ok", "id": emp.employee_id}


@router.get("/employees")
def get_employees(department: Optional[str] = None):
    if department:
        emps = list(crud.list_by_department(department))
    else:
        emps = list(crud.list_all())

    for e in emps:
        e["_id"] = str(e["_id"])  
    return {"count": len(emps), "results": emps}

