from sqlmodel import Session, create_engine, SQLModel, delete
from fastapi.testclient import TestClient
from main import app
from db import get_session
from models import URL, Visits
from dotenv import load_dotenv
import os

load_dotenv(".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL, echo=True)
SQLModel.metadata.create_all(test_engine)


def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


def clear_test_db():
    with Session(test_engine) as session:
        session.exec(delete(Visits))
        session.exec(delete(URL))
        session.commit()
