from sqlalchemy.orm import Session
from app.schemas.machine import MachineIn
from app.models.machine import Machine


def get_all(db: Session) -> list[Machine]:
    return db.query(Machine).all()

def get_by_id(db: Session, machine_id: int) -> Machine | None:
    return db.query(Machine).filter(Machine.id == machine_id).first()

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
        return None

    db.delete(machine)
    db.commit()
    return True