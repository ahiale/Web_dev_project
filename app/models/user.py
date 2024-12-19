from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from app.models.ticket import Ticket
from app.models.comment import Comment

# Table Users
class User(Base):
    __tablename__ = 'users'  

    id = Column(Integer, primary_key=True)  
    name = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)  
    email = Column(String(100), unique=True, nullable=False)  
    password = Column(String(100), nullable=False)  

    # # Relation 1 à N avec la table Ticket 
    tickets = relationship("Ticket", back_populates="user")

    # # Relation 1 à N avec la table Comment 
    comments = relationship("Comment", back_populates="user")
    