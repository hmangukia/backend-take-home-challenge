from sqlmodel import SQLModel, Field
from datetime import datetime

class URL(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    slug: str = Field(index=True, unique=True)
    long_url: str
    created_at: datetime = Field(default=datetime.utcnow)

class Visits(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    url_id: int = Field(foreign_key="url.id")
    visit_time: datetime = Field(default=datetime.utcnow)