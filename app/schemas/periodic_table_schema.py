from pydantic import BaseModel
from typing import Optional


class ElementSchema(BaseModel):
    atomicNumber: int
    atomicWeight: float
    boilingPoint: float
    valence: int
    meltingPoint: float
    symbol: str
    density: float
    atomicStructure: str
    name: str
    group: int
    period: int
    category: str
    funFact: str
    image: Optional[str] = None
