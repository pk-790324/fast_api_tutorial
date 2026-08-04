from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from database import create_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("Database tables created")
    yield
    print("Application shutdown")
    



app=FastAPI(
    title="Dabbawala Delivery app",
    description="API for managing dabbawala deliveries and tracking orders status",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(orders_router)
app.include_router(stats_router)


@app.get("/")
def get():
    return {"Dabbawala":"Welcome to dabbawala project"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )