from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # Fonction pour récupérer une session DB
from app.services.biomeService import BiomeService
from app.schemas.biomeSchema import BiomeRead

router = APIRouter()

@router.get("/biomes", response_model=List[BiomeRead])
def read_biomes(db: Session = Depends(get_db)):
    """
    Retourne tous les biomes.
    """
    biomes = BiomeService.read(db)
    return biomes

@router.get("/biomes/{biome_id}", response_model=BiomeRead)
def get_biome_by_id(biome_id: int, db: Session = Depends(get_db)):
    """
    Retourne un biome spécifique par ID.
    """
    biome = BiomeService.get_biome_by_id(db, biome_id)
    if not biome:
        raise HTTPException(status_code=404, detail="Biome non trouvé")
    return biome
