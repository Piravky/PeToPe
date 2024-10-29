from fastapi import FastAPI
import uvicorn
from routers import users, dog, cat
# from routers.users import router as users_router
# from routers.dog import router as dog_router
# from routers.cat import router as cat_router

app = FastAPI(
    title="PeToPe"
)
app.include_router(users.router)
app.include_router(dog.router)
app.include_router(cat.router)
# app.include_router(users_router)
# app.include_router(dog_router)
# app.include_router(cat_router)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8001)
