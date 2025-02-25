import asyncio
from datetime import datetime
from fastapi import APIRouter
from ..db import handle_user_visit_bot_async
from ..models import UserVisit


route_home = APIRouter()


@route_home.get("/")
async def home():
    current_datetime = datetime.now()
    user: UserVisit = UserVisit('7938711921', 'Đức', 'Trung', current_datetime, current_datetime, 1, False)
    result = await handle_user_visit_bot_async(user)
    return {"message": "Welcome to the FastAPI API!",
            "result": result}
