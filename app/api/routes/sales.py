from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.sales_record import SalesRecordOut
from app.crud import sales_record as sales_crud
from app.api.deps import require_roles
from app.models.sales_record import SalesRecord


router = APIRouter(prefix="/salesRecords", tags=["sales"])


def to_sales_out(s: SalesRecord) -> SalesRecordOut:
    return SalesRecordOut(
        id= s.id,
        machineId = s.machine_id,
        region=s.region,
        quantitySold = s.quantity_sold,
        revenue = float(s.revenue),
        saleDate = s.sale_date,
        dealerName = s.dealer_name
    )


@router.get("", response_model= list[SalesRecordOut], dependencies=[Depends(require_roles("admin", "stakeholder"))])
def list_sales(db: Session = Depends(get_db)):
    return [to_sales_out(s) for s in sales_crud.get_all(db)]