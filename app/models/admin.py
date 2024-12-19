import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from app.models.animal import Animal

# Classe Admin
class Admin(Base):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)  
    # Relation 1 à n avec enclos
    enclos = relationship("Enclos", back_populates="admin")
    animals = relationship("Animal", back_populates="admin")
