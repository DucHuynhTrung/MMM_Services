from fastapi import APIRouter
from ..db import select
from ..models import UserVisit


route_home = APIRouter()


@route_home.get("/")
async def home():
    query = "select * from UserVisit"
    result = select(query, class_convert=UserVisit)
    return {"message": "Welcome to the FastAPI API!",
            "result": result}
