from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="GateFlow",
    description="Lightweight API Gateway & Rate Limiter",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GateFlow"
    }