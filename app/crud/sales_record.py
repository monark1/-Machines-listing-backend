from sqlalchemy.orm import Session
from app.models.sales_record import SalesRecord


def get_all(db: Session) -> list[SalesRecord]:
    return db.query(SalesRecord).all()