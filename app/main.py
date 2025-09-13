from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routes import router

# Configure FastAPI with proper security scheme
app = FastAPI(
    title="Employee Management API",
    description="Employee Management System with JWT Authentication",
    version="1.0.0"
)

@app.get("/")   #  homepage, 
def homepage():
    return {"message": "FastAPI is running , pls go /docs for swagger UI"}

# include router
app.include_router(router)
