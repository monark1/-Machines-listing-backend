from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from schemas.sales_record import salesRecordOut
from app.crud import sales_record as sales_crud
from app.api.deps import require_roles
from app.models.sales_record import SalesRecord


router = APIRouter(prefix="/salesRecords", tags=["sales"])


def to_Sales_out(s: SalesRecord) -> salesRecordOut:
    return salesRecordOut(
        id= s.id,
        machine_id = s.machine_id,
        quantitySold = s.quantity_sold,
        revenue = float(s.revenue),
        saleDate = s.sale_date,
        dealername = s.dealer_name
    )


@router.get("", response_model= list[salesRecordOut], dependencies=[Depends(require_roles("admin", "stakeholder"))])
def list_sales(db: Session = Depends(get_db)):
    return [to_Sales_out(s for s in sales_crud.get_all(db))]