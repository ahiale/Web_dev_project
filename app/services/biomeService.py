from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.biome import Biome  # Importer la table Biome
from app.schemas.biomeSchema import BiomeCreate  # Importer les schémas

class BiomeService:
    @staticmethod
    def read(db: Session) -> List[Biome]:
        """
        Retourne la liste de tous les biomes.
        """
        return db.query(Biome).all()

    @staticmethod
    def get_biome_by_id(db: Session, biome_id: int) -> Optional[Biome]:
        """
        Récupère un biome par son ID.
        """
        return db.query(Biome).filter(Biome.id == biome_id).first()
