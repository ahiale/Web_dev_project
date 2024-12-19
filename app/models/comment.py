from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from app.models.enclos import Enclos


class Comment(Base):
    __tablename__ = 'comments'  

    id = Column(Integer, primary_key=True, index=True)  
    content = Column(String(255), nullable=False)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    enclos_id = Column(Integer, ForeignKey("enclos.id"), nullable=False)

    # Relation inverse de la relation User-Comment (N à 1) : chaque commentaire est lié à un utilisateur
    user = relationship("User", back_populates="comments")
    enclos = relationship("Enclos", back_populates="comments")
