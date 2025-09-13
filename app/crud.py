from app.configurations import employees_collection

def create_employee(data: dict):
    return employees_collection.insert_one(data)

def get_employee(employee_id: str):
    return employees_collection.find_one({"employee_id": employee_id})

def list_by_department(dept: str):
    return employees_collection.find({"department": dept}).sort("joining_date", -1)

def list_all():
    return employees_collection.find({})


