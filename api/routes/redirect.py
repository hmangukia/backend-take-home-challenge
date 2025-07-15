from models import URL, Visits
from db import get_session
from sqlmodel import Session, select
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime

router = APIRouter()

@router.get("/{slug}")
def redirect(slug: str, session: Session = Depends(get_session)):
    # checks if the slug exists in the database. If not, raise a 404 error
    url = session.exec(select(URL).where(slug == URL.slug)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    # logs the visit to the database
    visit = Visits(url_id=url.id, visit_time=datetime.utcnow())
    session.add(visit)
    session.commit()
    session.refresh(visit)
    
    # redirects the user to the original long URL
    return RedirectResponse(url.long_url, status_code=307)
