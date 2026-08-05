from fastapi import FastAPI
import uvicorn

from database import init_db

from routes.contracts import router as contracts_router

app=FastAPI(
    title="Vakeel Contract API",
    description="Ai-powered contract analysis",
    version="1.0.0"
)



@app.on_event("startup")
async def startup_event():
    init_db()
    








@app.get("/")
async def root():
    return{
        "app":"AI-Powered contract analysis"
    }
    

app.include_router(contracts_router)
    
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )