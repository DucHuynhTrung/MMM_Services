from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from .services import run_polling_telegram, stop_polling_telegram
from .routes import route_home

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    run_polling_telegram()


@app.on_event("shutdown")
async def shutdown_event():
    stop_polling_telegram()


app.include_router(route_home)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
