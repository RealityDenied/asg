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


@router.get("/employees/avg-salary")
def avg_salary():
    res = crud.avg_salary_by_department()
    data = []
    for r in res:
        data.append({"dept": r["_id"], "avg": r["avg_salary"]})
    return data


@router.get("/employees/search")
def search_employees(skill: str):
    results = list(crud.search_by_skill(skill))
    for r in results:
        r["_id"] = str(r["_id"])
    return results


@router.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    emp = crud.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")
    emp["_id"] = str(emp["_id"])
    return emp


@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, emp: UpdateEmployee):
    update_data = emp.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    
    crud.update_employee(employee_id, update_data)
    return {"updated": True, "employee_id": employee_id}


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    deleted = crud.delete_employee(employee_id)
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"deleted": True}
