from sqlalchemy import Column,String,Integer,Boolean, ForeignKey,Date
from database import Base
from sqlalchemy.orm import relationship

class Ticket(Base):
    __tablename__ = 'tickets'  

    id = Column(Integer, primary_key=True, index=True)  
    price = Column(Integer, nullable=False)  
    qte= Column(Integer)
    dateticket=Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    compte_id = Column(Integer, ForeignKey("comptes.id"), nullable=False)  # Compte associé au ticket

    # Relations
    user = relationship("User", back_populates="tickets")
    compte = relationship("Compte", back_populates="tickets")
