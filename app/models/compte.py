from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Compte(Base):
    __tablename__ = 'comptes'

    id = Column(Integer, primary_key=True, index=True)
    numero_compte = Column(String(50), unique=True, nullable=False)
    solde = Column(Float, default=10.0)  # Initialisation du solde à 10 euros
    
    # Relation entre Compte et Ticket (un compte peut être associé à plusieurs tickets)
    tickets = relationship("Ticket", back_populates="compte")
