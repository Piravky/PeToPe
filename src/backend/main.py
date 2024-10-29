from fastapi import FastAPI
import uvicorn
from routers import users, dog, cat

app = FastAPI(
    title="PeToPe"
)

app.include_router(users.router) 
app.include_router(dog.router)
app.include_router(cat.router)

@app.get("/")
async def root():
    return {'message': "hello PeToPe"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
