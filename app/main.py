from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.init_db import create_first_superuser

app = FastAPI(
    title=settings.APP_NAME,
    description="API для сервиса доставки",
    version="0.1.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    await create_first_superuser()

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в DeliveryAPI!"}