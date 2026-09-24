from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.query_utils import apply_sort, paginate
from app.models.machine import Machine
from app.models.sales_record import SalesRecord

SORTABLE_FIELDS = {
    "region": "region",
    "quantitySold": "quantity_sold",
    "revenue": "revenue",
    "saleDate": "sale_date",
    "dealerName": "dealer_name",
}


def get_all_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    region: str | None = None,
    machine_id: int | None = None,
    search: str | None = None,
    sort: str | None = None,
    order: str = "asc",
) -> tuple[list[SalesRecord], int]:
    query = db.query(SalesRecord).options(joinedload(SalesRecord.machine))

    needs_join = bool(search) or sort == "machineName"
    if needs_join:
        query = query.join(Machine, SalesRecord.machine_id == Machine.id)

    if region:
        query = query.filter(SalesRecord.region == region)
    if machine_id:
        query = query.filter(SalesRecord.machine_id == machine_id)

    if search:
        query = query.filter(or_(
            SalesRecord.dealer_name.ilike(f"%{search}%"),
            SalesRecord.region.ilike(f"%{search}%"),
            Machine.name.ilike(f"%{search}%"),
        ))

    if sort == "machineName":
        query = query.order_by(Machine.name.desc() if order == "desc" else Machine.name.asc())
    else:
        sort_column = SORTABLE_FIELDS.get(sort) if sort else None
        query = apply_sort(query, SalesRecord, sort_column, set(SORTABLE_FIELDS.values()), order)

    return paginate(query, page, page_size)