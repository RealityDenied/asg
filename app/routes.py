from fastapi import APIRouter, HTTPException
from typing import Optional
from app import crud
from app.models import Employee, UpdateEmployee
from app.utils import get_collection_indexes, get_index_stats



router = APIRouter()

@router.post("/employees")
def create_employee(emp: Employee):
    # check if employee already exists
    existing_emp  = crud.get_employee(emp.employee_id)
    if existing_emp:
        raise  HTTPException(status_code=400, detail="Employee already exists with this ID")
    
    result=crud.create_employee(emp.dict())
    return {"status": "ok", "id": emp.employee_id}



@router.get("/employees")
def get_employees(
    department: Optional[str] = None,
    page:  int = 1,
    limit: int = 10
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
def avg_salary():
    res = crud.avg_salary_by_department()
    data= []
    for r in res:
        data.append({"dept": r["_id"], "avg": r["avg_salary"]})
    return data


@router.get("/employees/search")
def search_employees(skill: str):
    results = list(crud.search_by_skill(skill))
    for r in results:
        r["_id"]= str(r["_id"])
    return results


@router.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    emp = crud.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")
    emp["_id"]= str(emp["_id"])
    return emp


@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, emp: UpdateEmployee):
    update_data= emp.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    
    crud.update_employee(employee_id, update_data)
    return {"updated": True, "employee_id": employee_id}


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
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
