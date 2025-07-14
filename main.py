from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import create_engine, SQLModel, Session
from models import URL, Visits

app = FastAPI()

engine = create_engine(f'postgresql://hetalmangukia:postgres@localhost:5432/postgres')

@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")