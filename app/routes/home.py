import asyncio
from fastapi import APIRouter
from ..db import add_to_queue
from ..models import UserVisit


route_home = APIRouter()


@route_home.get("/")
async def home():
    query = "select * from UserVisit"
    result = await add_to_queue(query, class_convert=UserVisit, as_dict=True, return_result=True)
    return {"message": "Welcome to the FastAPI API!",
            "result": result}
