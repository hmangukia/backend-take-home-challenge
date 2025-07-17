from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from api.main import api_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")


app.include_router(api_router)
