from datetime import date, datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import ticket, compte, user
from app.models.user import User
from app.models.compte import Compte
from app.models.ticket import Ticket
from fastapi import HTTPException, status, Depends

from database import get_db


def create_ticket_from_compte(numero_compte: str, user_id: int, dateticket: date, qte: int, db: Session):
    price = 10  # Prix fixe d'un ticket en euros
    dateticket = datetime.strptime("2024-11-10", "%Y-%m-%d").date()
    
    compte = db.query(Compte).filter(Compte.numero_compte == numero_compte).first()
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    
   
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérifier si le solde est suffisant
    total_price = price * qte  
    if compte.solde < total_price:
        raise HTTPException(status_code=400, detail="Solde insuffisant pour effectuer l'achat")
    
   
    try:
        # Décrémenter le solde du compte
        compte.solde -= total_price
        
       
        new_ticket = Ticket(
            price=price,  
            qte=qte,            
            dateticket=dateticket,  
            user_id=user.id,    
            compte_id=compte.id  
        )
        
        
        db.add(new_ticket)
        db.commit()  
        
        # Retourner une confirmation avec les détails du ticket créé
        return {
            "message": "Ticket créé avec succès",
            "ticket_id": new_ticket.id,
            "total_prix": total_price,
            "nouveau_solde": compte.solde
        }
    
    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Erreur lors de la création du ticket: " + str(e))
    
# Obtenir un ticket par son ID
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket non trouvé")
    return ticket

# Obtenir tous les animaux
def get_all_tickets(db: Session = Depends(get_db)):
    try:
        logging.info("Récupération de tous les animaux de la base de données")
        tickets_list = db.query(Ticket).all()
        logging.info(f"{len(tickets_list)} animaux récupérés")
        return tickets_list
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des animaux : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")