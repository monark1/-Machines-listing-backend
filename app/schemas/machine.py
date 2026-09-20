from pydantic import BaseModel


class MachineSpecs(BaseModel):
    width: int
    speed: int
    printColors: int


class MachineIn(BaseModel):
    name: str
    category: str
    launchYear: int
    status: str
    unitPrice: float
    specs: MachineSpecs


class MachineOut(MachineIn):
    id: int
