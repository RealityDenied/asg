from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Employee Management API")

@app.get("/")
def homepage():
    return {"message": "FastAPI is running , pls go to /docs for opening Swagger UI "}


app.include_router(router, tags=["employees"])
