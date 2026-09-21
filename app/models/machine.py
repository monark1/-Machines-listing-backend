import enum
from sqlalchemy import Column, Integer, String, Numeric, Enum
from app.db.base import Base


class MachineStatus(str, enum.Enum):
    active = "active"
    discontinued = "discontinued"


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    launch_year = Column(Integer, nullable=False)
    status = Column(Enum(MachineStatus), nullable=False, default=MachineStatus.active)
    unit_price = Column(Numeric(14, 2), nullable=False)

    width = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    print_colors = Column(Integer, nullable=False)
