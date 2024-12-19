from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import date
from app.models import ticket, user, compte
from app.models.ticket import Ticket
from app.models.user import User
from app.models.compte import Compte
from database import get_db
from app.services.ticketService import create_ticket_from_compte, get_all_tickets, get_ticket

router = APIRouter()

@router.post("/create_ticket")
def create_ticket(
    numero_compte: str,
    user_id: int,
    dateticket: date,
    qte: int,
    db: Session = Depends(get_db)
):
    """
    Crée un ticket pour un utilisateur via un numéro de compte donné,
    le prix est automatiquement débité du compte si le solde est suffisant.
    """
    try:
        response = create_ticket_from_compte(
            numero_compte=numero_compte,
            user_id=user_id,
            dateticket=dateticket,
            qte=qte,
            db=db
        )
        return response  # Retourne la réponse du service (confirmation, ticket créé, etc.)
    except HTTPException as e:
        # Si une erreur survient (ex: solde insuffisant, compte non trouvé, etc.)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    

@router.get("/tickets", status_code=status.HTTP_200_OK)
def read_all_tickets(db: Session = Depends(get_db)):
    try:
        tickets_list = get_all_tickets(db)
        if not tickets_list:
            raise HTTPException(status_code=404, detail="No tickets found")
        return tickets_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        ticket = get_ticket(ticket_id, db)
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))