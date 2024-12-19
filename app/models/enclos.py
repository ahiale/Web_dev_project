from sqlalchemy import Column,String,Integer,Boolean, ForeignKey, Time
from database import Base
from sqlalchemy.orm import relationship
from app.models.admin import Admin
from app.models.animal import Animal

class Enclos(Base):
    __tablename__ = 'enclos'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    heuresD=Column(Time)
    heuresF=Column(Time)
    statut = Column(Boolean, default=True)   
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    biome_id = Column(Integer, ForeignKey("biomes.id"), nullable=False) 
    
    
    # Relation Enclos-Admin : chaque enclos est lié à un admin
    admin = relationship("Admin", back_populates="enclos")
    
    # Relation Enclos-Animaux : un enclos peut contenir plusieurs animaux
    animals = relationship("Animal", back_populates="enclos")
    
    # Relation Enclos-Comments : chaque enclos peut avoir plusieurs commentaires
    comments = relationship("Comment", back_populates="enclos")
    
    biome = relationship("Biome", back_populates="enclos")