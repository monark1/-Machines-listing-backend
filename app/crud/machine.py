from sqlalchemy.orm import Session
from app.schemas.machine import MachineIn
from app.models.machine import Machine
from app.core.query_utils import apply_search, apply_sort, paginate

SORTABLE_FIELDS = {
    "name": "name",
    "category": "category",
    "launchYear": "launch_year",
    "unitPrice": "unit_price",
    "status": "status",
}

SEARCHABLE_COLUMNS = ["name", "category"]


def get_all_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    category: str | None = None,
    status: str | None = None,
    search: str | None = None,
    sort: str | None = None,
    order: str = "asc",
) -> tuple[list[Machine], int]:
    query = db.query(Machine).filter(Machine.is_deleted.is_(False))

    if category:
        query = query.filter(Machine.category == category)
    if status:
        query = query.filter(Machine.status == status)

    query = apply_search(query, Machine, search, SEARCHABLE_COLUMNS)

    sort_column = SORTABLE_FIELDS.get(sort) if sort else None
    allowed = set(SORTABLE_FIELDS.values())
    query = apply_sort(query, Machine, sort_column, allowed, order)

    return paginate(query, page, page_size)


def get_by_id(db: Session, machine_id: int) -> Machine | None:
    return db.query(Machine).filter(Machine.id == machine_id, Machine.is_deleted == False).first()

def create(db: Session, machine: Machine) -> Machine:
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine

def update(db: Session, machine_id: int, payload: MachineIn) -> Machine | None:
    machine = get_by_id(db, machine_id)
    if machine is None: 
        return None

    machine.name = payload.name
    machine.status = payload.status
    machine.category = payload.category
    machine.launch_year = payload.launchYear
    machine.unit_price = payload.unitPrice
    machine.speed = payload.specs.speed
    machine.width = payload.specs.width
    machine.print_colors = payload.specs.printColors

    db.commit()
    db.refresh(machine)
    return machine

def delete(db: Session, machine_id: int) -> bool:
    machine = get_by_id(db, machine_id)
    if machine is None:
        return False

    machine.is_deleted = True
    db.commit()
    return True