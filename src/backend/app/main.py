from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
    )

# добавление роутеров
app.include_router(router)


# проверка доступности
@app.get("/health")
def get_root():
    return {"message":"ok"}