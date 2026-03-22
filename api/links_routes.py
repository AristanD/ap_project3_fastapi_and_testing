from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.session import get_db
from services.link_service import LinkService
from services.stats_service import StatsService
from repos.link_repo import LinkRepo
from api.deps import get_curr_user, get_curr_user_strict


router = APIRouter()

# Ручка создания короткой ссылки
@router.post("/links/shorten")
def create_link(data: dict, db: Session = Depends(get_db), user_id: int | None = Depends(get_curr_user)):
    
    repo = LinkRepo(db)
    service = LinkService(repo)

    link = service.create_link(
        data["orig_url"],
        data.get("custom_alias"),
        data.get("expires_dt"),
        user_id=user_id
    )

    return {
        "short_url": f"http://localhost:8000/{link.short_code}"
    }   # Короткая ссылка


# Ручка для вывода статистики
@router.get("/links/{short_code}/stats")
def get_stats(short_code: str, db: Session = Depends(get_db)):

    repo = LinkRepo(db)
    service = StatsService(repo)

    return service.get_stats(short_code)


# эндпоинт для удаления ссылки из бд
@router.delete("/links/{short_code}")
def delete_link(short_code: str, db: Session = Depends(get_db), user_id: int | None = Depends(get_curr_user)):

    repo = LinkRepo(db)
    service = LinkService(repo)

    deleted = service.delete_link(short_code, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Link not found")

    return {
        "message": "Link deleted successfully",
        "short_code": short_code
    }


# Ручка редиректа по ссылке (должна сделать запрос и привести на сайт)
@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    repo = LinkRepo(db)
    service = LinkService(repo)

    url = service.resolve_link(short_code)
    if not url:
        return {"error": "not found"}

    return RedirectResponse(url)


# Ручка для обновления оргинальной ссылки для алиаса пользователя или короткой сгенерированной
@router.put("/links/{short_code}")
def update_link(short_code: str, data: dict, db: Session = Depends(get_db), user_id: int | None = Depends(get_curr_user)):

    repo = LinkRepo(db)
    service = LinkService(repo)

    link = service.update_link(short_code, data["orig_url"], user_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"message": "Link updated", "short_code": short_code}


# Ручка для поиска алиаса ссылки по оригинальному URL
@router.get("/links/search")
def search_links(original_url: str, db: Session = Depends(get_db)):

    repo = LinkRepo(db)
    service = LinkService(repo)

    links = service.search_links(original_url)

    return links


# Ручка для вывода всех ссылок по проектам
@router.get("/links/{project}")
def search_project(project: str, db: Session = Depends(get_db)):

    repo = LinkRepo(db)
    service = LinkService(repo)

    links = service.search_project(project=project)

    return links