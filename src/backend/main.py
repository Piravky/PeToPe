from fastapi import FastAPI, APIRouter
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from routers import users, dog, cat
from auth.router import router

app = FastAPI(
    title="PeToPe",
    docs_url="/api/docs"
)
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники, можно указать конкретные URL
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)
v1 = APIRouter(prefix='/api/v1')
v1.include_router(users.router)
v1.include_router(dog.router)
v1.include_router(cat.router)
app.include_router(router)
app.include_router(v1)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
