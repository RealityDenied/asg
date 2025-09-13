from app.configurations import employees_collection

def create_employee(employee_data: dict):
    result = employees_collection.insert_one(employee_data)
    return result

def get_employee(emp_id: str):
    employee = employees_collection.find_one({"employee_id": emp_id})
    return employee

def update_employee(emp_id: str, update_data: dict):
    result =employees_collection.update_one({"employee_id": emp_id}, {"$set": update_data})
    return result

def delete_employee(emp_id: str):
    result = employees_collection.delete_one({"employee_id": emp_id})
    return result


def list_all(skip_records: int = 0, limit_records: int = 10):
    cursor = employees_collection.find({}).skip(skip_records).limit(limit_records)
    return cursor

def list_by_department(department_name: str, skip_records: int = 0, limit_records: int = 10):
    cursor = (
        employees_collection
        .find({"department": department_name})
        .sort("joining_date", -1)
        .skip(skip_records)
        .limit(limit_records)
    )
    return cursor

def count_all():
    total  =employees_collection.count_documents({})
    return total

def count_by_department(department_name: str):
    count= employees_collection.count_documents({"department":department_name})
    return count


def avg_salary_by_department():
    aggregation_pipeline= [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}
    ]
    result= employees_collection.aggregate(aggregation_pipeline)
    return result

def search_by_skill(skill_name: str):
    cursor =employees_collection.find({"skills":skill_name})
    return cursor
