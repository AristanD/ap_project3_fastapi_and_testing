from datetime import datetime, timezone, timedelta
from db.session import SessionLocal
from models.link import Link
from models.expired_link import ExpiredLink
from config import settings


def delete_expired_links():
    """Удаление истекающих ссылок, лучше запускать как background task"""

    db = SessionLocal()

    limit_date = datetime.now(timezone.utc) - timedelta(days=settings.DEFAULT_UNUSED_DAYS)  # Дата истечения срока

    links = db.query(Link).filter(Link.last_accessed_dt <= limit_date).all()   # Автоудаление всех неиспользуемых ссылок спустя 14 дней

    for link in links:
        # Сначала добавляю в таблицу expired, потом удалю из основной таблицы (получается эдакая корзина)
        expired = ExpiredLink(
            orig_url=link.orig_url,
            short_code=link.short_code,
            expired_at=datetime.now(timezone.utc)
        )
        
        db.add(expired)
        db.delete(link)

    db.commit()
    db.close()