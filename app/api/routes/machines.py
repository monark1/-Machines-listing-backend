from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.machine import MachineIn, MachineOut, MachineSpecs
from app.crud import machine as machine_crud
from app.api.deps import require_roles, get_current_user
from app.models.machine import Machine
from app.schemas.pagination import PaginatedResponse

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


@router.get("", response_model=PaginatedResponse[MachineOut], dependencies=[Depends(get_current_user)])
def list_machines(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    category: str | None = None,
    status_: str | None = Query(None, alias="status"),
    search: str | None = None,
    sort: str | None = None,
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    machines, total = machine_crud.get_all_paginated(
        db,
        page=page,
        page_size=page_size,
        category=category,
        status=status_,
        search=search,
        sort=sort,
        order=order,
    )
    return PaginatedResponse[MachineOut](
        items=[to_machine_out(m) for m in machines],
        total=total,
        page=page,
        pageSize=page_size,
        totalPages=max(1, -(-total // page_size)),
    )


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
