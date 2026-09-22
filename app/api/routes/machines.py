from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.machine import MachineIn, MachineOut, MachineSpecs
from app.crud import machine as machine_crud
from app.api.deps import require_roles, get_current_user
from app.models.machine import Machine

router = APIRouter(prefix="/machines", tags=["machines"])


def to_machine_out(m: Machine) -> MachineOut:
    return MachineOut(
        id=m.id,
        name=m.name,
        category=m.category,
        launchYear=m.launch_year,
        status=m.status.value,
        unitPrice=float(m.unit_price),
        specs=MachineSpecs(width=m.width, speed=m.speed, printColors=m.print_colors),
    )


@router.get("", response_model=list[MachineOut], dependencies=[Depends(get_current_user)])
def list_machines(db: Session = Depends(get_db)):
    return [to_machine_out(m) for m in machine_crud.get_all(db)]


@router.get("/{machine_id}", response_model=MachineOut, dependencies=[Depends(get_current_user)])
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    machine = machine_crud.get_by_id(db, machine_id)
    if machine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    return to_machine_out(machine)


@router.post("", response_model=MachineOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
def create_machine(payload: MachineIn, db: Session = Depends(get_db)):
    machine = Machine(
        name=payload.name,
        category=payload.category,
        launch_year=payload.launchYear,
        status=payload.status,
        unit_price=payload.unitPrice,
        width=payload.specs.width,
        speed=payload.specs.speed,
        print_colors=payload.specs.printColors,
    )
    created = machine_crud.create(db, machine)
    return to_machine_out(created)


@router.put("/{machine_id}", response_model=MachineOut, dependencies=[Depends(require_roles("admin"))])
def update_machine(machine_id: int, payload: MachineIn, db: Session = Depends(get_db)):
    updated = machine_crud.update(db, machine_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
    return to_machine_out(updated)


@router.delete("/{machine_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    deleted = machine_crud.delete(db, machine_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
