from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel


class URL(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    slug: str = Field(index=True, unique=True, nullable=False)
    long_url: str = Field(index=True, unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Visits(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    url_id: int = Field(foreign_key="url.id")
    visit_time: datetime = Field(default_factory=datetime.utcnow)


class ShortenUrlRequest(BaseModel):
    long_url: str


class ShortenUrlResponse(BaseModel):
    short_url: str
    slug: str


class URLStatsResponse(BaseModel):
    slug: str
    long_url: str
    visits: int
    last_visit: datetime | None


class FlyerRequest(BaseModel):
    prompt: str
