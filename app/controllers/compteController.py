from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.compteService import CompteService
from app.schemas.compteSchema import CompteCreate  # Assurez-vous d'avoir le schéma nécessaire
from database import get_db

router = APIRouter()

# POST /compte/create - Créer un nouveau compte
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_compte_controller(compte_create: CompteCreate, db: Session = Depends(get_db)):
    """
    Endpoint pour créer un compte avec un numéro et un solde initial.
    """
    try:
        response = CompteService.creer_compte(db=db, numero_compte=compte_create.numero_compte)
        if 'error' in response:
            raise HTTPException(status_code=500, detail=response['error'])
        return response  # Retourne le message de succès et les informations du compte
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du compte: {str(e)}")

