from fastapi import FastAPI
import uvicorn

from app.routes.query import router as query_router

app=FastAPI(
    title="RAG API",
    description="this is a rag api that alllow you to interact with a pdf ",
    version="0.1.0"
)

app.include_router(query_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )