from app.configurations import employees_collection

def create_employee(data: dict):
    return employees_collection.insert_one(data)

def get_employee(employee_id: str):
    return employees_collection.find_one({"employee_id": employee_id})

def list_by_department(dept: str):
    return employees_collection.find({"department": dept}).sort("joining_date", -1)

def list_all():
    return employees_collection.find({})

def avg_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}
    ]
    return employees_collection.aggregate(pipeline)

def search_by_skill(skill: str):
    return employees_collection.find({"skills": skill})



