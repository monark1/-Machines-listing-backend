from datetime import date
from pydantic import BaseModel


class SalesRecordOut(BaseModel):
    id: int
    machineId: int
    region: str
    quantitySold: int
    revenue: float
    saleDate: date
    dealerName: str
