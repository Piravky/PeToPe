from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from routers import users, dog, cat


app = FastAPI(
    title="PeToPe"
)

# Настройка CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники, можно указать конкретные URL
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)
app.include_router(users.router)
app.include_router(dog.router)
app.include_router(cat.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
