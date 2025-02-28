import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .services import run_polling_telegram, stop_polling_telegram
from .apis import route_home
from .db import start_query_workers


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_query_workers()
    await run_polling_telegram()
    yield
    await stop_polling_telegram()


app = FastAPI(lifespan=lifespan)

app.include_router(route_home)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
