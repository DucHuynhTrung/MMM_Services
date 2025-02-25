import asyncio, threading
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .services import run_polling_telegram, stop_polling_telegram
from .routes import route_home
from .db import start_query_workers

executor = ThreadPoolExecutor(max_workers=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_query_workers()
    # loop = asyncio.get_running_loop()
    # polling_task = loop.run_in_executor(executor, run_polling_telegram)

    yield  # Chạy server FastAPI

    # Khi server shutdown, dừng polling
    # stop_polling_telegram()
    # await polling_task  # Đợi polling dừng hoàn toàn

app = FastAPI(lifespan=lifespan)

app.include_router(route_home)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
