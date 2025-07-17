from models import URL, Visits
from db import get_session
from sqlmodel import Session, select
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import BackgroundTasks

router = APIRouter()


@router.get("/{slug}")
async def redirect(
    slug: str,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    # checks if the slug exists in the database. If not, raise a 404 error
    url = session.exec(select(URL).where(slug == URL.slug)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    # logs the visit to the database
    background_tasks.add_task(log_visit, url.id, session)

    # redirects the user to the original long URL
    return RedirectResponse(url.long_url, status_code=307)


def log_visit(url_id: int, session: Session):
    visit = Visits(url_id=url_id)
    session.add(visit)
    session.commit()
