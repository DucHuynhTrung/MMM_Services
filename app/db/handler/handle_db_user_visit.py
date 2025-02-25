import os
from datetime import datetime
from ..base import put_queue_async
from ...models import UserVisit
from dotenv import load_dotenv

load_dotenv()

async def handle_user_visit_bot_async(user: UserVisit) -> bool:
    result: bool = False
    user_find = await find_user_visit_async(user.ID)
    if user_find:
        rows_update = await update_user_visit_async(datetime.now(), user_find.TotalVisit + 1, user.ID)
        if rows_update: 
            result = True
    else:
        rows_insert = await insert_user_visit_async(user)
        if rows_insert: 
            result = True

    return result


async def find_user_visit_async(ID: str) -> UserVisit | None:
    query_string: str = os.getenv('USER_VISIT_FIND_ID').__str__()
    result = await put_queue_async(query=query_string, params=(ID,), class_convert=UserVisit, fetch_one=True)
    if type(result) is UserVisit:
        return result
    return None


async def insert_user_visit_async(user: UserVisit) -> int | None:
    query_string: str = os.getenv('USER_VISIT_INSERT').__str__()
    rows_insert = await put_queue_async(query=query_string, params=(user.ID, user.FirstName, user.LastName, user.DateVisit, user.LastVisit, user.TotalVisit, user.IsSignin, user.DateSignin))
    if type(rows_insert) is int:
        return rows_insert
    return None


async def update_user_visit_async(LastVisit: datetime, TotalVisit: int, ID: str) -> int | None:
    query_string: str = os.getenv('USER_VISIT_UPDATE').__str__()
    rows_update = await put_queue_async(query=query_string, params=(LastVisit, TotalVisit, ID))
    if type(rows_update) is int:
        return rows_update
    return None

