
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from . import models
from .routers import router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RisparmioSmart Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
