from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, dashboard_router
from app.config import settings


app = FastAPI()


app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.allowed_origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
    )

# добавление роутеров
app.include_router(auth_router)
app.include_router(dashboard_router)


# проверка доступности
@app.get("/health")
def get_root():
    return {"message":"ok"}