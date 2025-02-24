from fastapi import APIRouter
from ..db import select


route_home = APIRouter()


@route_home.get("/")
async def home():
    query = "select * from UserVisit"
    result = select(query)
    return {"message": "Welcome to the FastAPI API!",
            "result": result}
