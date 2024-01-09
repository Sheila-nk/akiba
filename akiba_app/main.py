from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import model
from .database import engine
from .routers import router

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="akiba_app/static"), name="static")

@app.get("/")
async def index():
    return {"message": "Hello World"}
       
app.include_router(router)
