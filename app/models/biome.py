from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Biome(Base):
    __tablename__ = 'biomes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    color = Column(String(20), nullable=False)
    
    # Relation Biome-Enclos : un biome peut contenir plusieurs enclos
    enclos = relationship("Enclos", back_populates="biome")
