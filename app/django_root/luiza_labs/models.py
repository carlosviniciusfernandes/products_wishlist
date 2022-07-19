from dataclasses import dataclass
from typing import Optional
from uuid import uuid4


@dataclass
class Product:
    id: uuid4
    price: float
    image: str
    brand: str
    title: str
    reviewScore: Optional[float] = None
