from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Employee Management API")

@app.get("/")   #  homepage, 
def homepage():
    return {"message": "FastAPI is running , pls go /docs for swagger UI"}



# include router
app.include_router(router)
