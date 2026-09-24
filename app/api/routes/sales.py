from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.crud import sales_record as sales_crud
from app.db.session import get_db
from app.models.sales_record import SalesRecord
from app.schemas.pagination import PaginatedResponse
from app.schemas.sales_record import SalesRecordOut

router = APIRouter(prefix="/salesRecords", tags=["sales"])


def to_sales_out(s: SalesRecord) -> SalesRecordOut:
    return SalesRecordOut(
        id=s.id,
        machineId=s.machine_id,
        machineName=s.machine.name if s.machine else "Unknown",
        region=s.region,
        quantitySold=s.quantity_sold,
        revenue=float(s.revenue),
        saleDate=s.sale_date,
        dealerName=s.dealer_name,
    )


@router.get("", response_model=PaginatedResponse[SalesRecordOut], dependencies=[Depends(require_roles("admin", "stakeholder"))],
)
def list_sales(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    region: str | None = None,
    machine_id: int | None = Query(None, alias="machineId"),
    search: str | None = None,
    sort: str | None = None,
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    sales, total = sales_crud.get_all_paginated(
        db,
        page=page,
        page_size=page_size,
        region=region,
        machine_id=machine_id,
        search=search,
        sort=sort,
        order=order,
    )
    return PaginatedResponse[SalesRecordOut](
        items=[to_sales_out(s) for s in sales],
        total=total,
        page=page,
        pageSize=page_size,
        totalPages=max(1, -(-total // page_size)),
    )