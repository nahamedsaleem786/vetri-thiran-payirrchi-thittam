from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(
    title="LegalEase API",
    description="AI-assisted legal document generator",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "LegalEase API is running",
        "status": "success",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }


app.include_router(router)
