from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: Union[datetime, str]   
    skills: List[str]

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[datetime] = None  
    skills: Optional[List[str]] = None

# Authentication models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
