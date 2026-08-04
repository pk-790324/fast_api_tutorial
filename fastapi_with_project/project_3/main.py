from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables

from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("database tables created")
    yield
    # shutdown:cleanup
    print("Shutting down the app")
    





app=FastAPI(
    title="Rangmanch Review API",
    description="Theatre review API for pune Rangmanch",
    lifespan=lifespan
)

app.include_router(reviews_router)

# Add all the API endpoints defined in review_router to this application

@app.get("/")
def get():
    return {"hello":"hi"}
