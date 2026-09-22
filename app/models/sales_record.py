from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class SalesRecord(Base):
    __tablename__ = "sales_records"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    region = Column(String(50), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    revenue = Column(Numeric(14, 2), nullable=False)
    sale_date = Column(Date, nullable=False)
    dealer_name = Column(String(150), nullable=False)
    machine = relationship("Machine")