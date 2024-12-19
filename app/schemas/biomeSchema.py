from pydantic import BaseModel
from typing import List, Optional

# Schéma pour la création de Biome
class BiomeCreate(BaseModel):
    name: str
    color: str

# Schéma pour la lecture de Biome
class BiomeRead(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        orm_mode = True
