from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Animal(Base):
    __tablename__ = 'animals'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description =Column(String(500), nullable=False)
    picture=Column(String(100), nullable=False)
    enclos_id = Column(Integer, ForeignKey("enclos.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    
    # Relation Animaux-Enclos : chaque animal est lié à un enclos
    enclos = relationship("Enclos", back_populates="animals")
    admin = relationship("Admin", back_populates="animals")