from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables

from routes.student import router as student_router

import uvicorn

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("database tables created")
    yield
    # shutdown:clean up
    print("Shutting down the app")
    

app=FastAPI(
    title="Student details API",
    description="student details of ABC College",
    lifespan=lifespan
)

app.include_router(student_router)

# Add all the API endpoinst defined in student_router to this application

@app.get("/")
def get():
    return {"student":"Welcome to student database"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )