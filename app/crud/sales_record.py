from sqlalchemy.orm import Session, joinedload
from app.models.sales_record import SalesRecord


def get_all(db: Session) -> list[SalesRecord]:
    return db.query(SalesRecord).options(joinedload(SalesRecord.machine)).all()