from fastapi import FastAPI
from app.api.endpoints import user

app = FastAPI()

app.include_router(user.router, tags=["User Operations"], prefix="/users")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "ALIVE!"}
