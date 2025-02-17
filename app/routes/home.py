from fastapi import APIRouter

route_home = APIRouter()


@route_home.get("/")
async def home():
    return {"message": "Welcome to the FastAPI API!"}
