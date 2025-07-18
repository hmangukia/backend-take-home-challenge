from models import URL, Visits
from db import get_session, engine
from sqlmodel import Session, select
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import BackgroundTasks

router = APIRouter()


@router.get("/{slug}")
async def redirect_to_long_url(
    slug: str,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    """
    Redirects to the original long URL based on the provided slug.

    Args:
        slug (str): The slug of the URL to redirect to.
        background_tasks (BackgroundTasks): FastAPI background tasks manager.
        session (Session): Database session dependency to access the database.

    Raises:
        HTTPException: Raises 404 if the slug is not found in the database.

    Returns:
        RedirectResponse: A response that redirects to the original long URL with a 307 status code.
    """
    # checks if the slug exists in the database. If not, raise a 404 error
    url = session.exec(select(URL).where(slug == URL.slug)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    # logs the visit to the database asynchronously
    background_tasks.add_task(log_visit, url.id)

    # redirects the user to the original long URL
    return RedirectResponse(url.long_url, status_code=307)


def log_visit(url_id: int):
    """
    Logs a visit for a URL to the database asynchronously.

    Args:
        url_id (int): The ID of the URL that was visited.
        session (Session): Database session dependency to access the database.
    """
    try:
        with Session(engine) as session:
            visit = Visits(url_id=url_id)
            session.add(visit)
            session.commit()
    except Exception as e:
        print(f"Error logging visit: {e}")
