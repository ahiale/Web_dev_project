from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..models.enclos import Enclos
from ..schemas.enclosSchema import EnclosCreate, EnclosUpdate
from database import get_db
import logging

def retrieve_enclos(enclos_id: int, db: Session = Depends(get_db)):
    return db.query(Enclos).filter(Enclos.id == enclos_id).first()

def get_enclos(enclos_id: int, db: Session = Depends(get_db)):
    enclos = db.query(Enclos).filter(Enclos.id == enclos_id).first()
    if not enclos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enclos non trouvé")
    return enclos

def create_enclos(enclos: EnclosCreate, db: Session = Depends(get_db)):
    db_enclos = Enclos(
        name=enclos.name,
        heuresD=enclos.heuresD,
        heuresF=enclos.heuresF,
        statut=enclos.statut,
        admin_id=enclos.admin_id,
        biome_id=enclos.biome_id
    )
    
    try:
        db.add(db_enclos)
        db.commit()
        db.refresh(db_enclos)
        return db_enclos
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'enclos : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

def update_enclos(enclos_id: int, enclos_update: EnclosUpdate, db: Session = Depends(get_db)):
    enclos = db.query(Enclos).filter(Enclos.id == enclos_id).first()
    
    if not enclos:
        raise HTTPException(status_code=404, detail=f"Enclos avec l'ID {enclos_id} non trouvé")
    
    enclos.name = enclos_update.name if enclos_update.name else enclos.name
    enclos.heuresD = enclos_update.heuresD if enclos_update.heuresD else enclos.heuresD
    enclos.heuresF = enclos_update.heuresF if enclos_update.heuresF else enclos.heuresF
    enclos.statut = enclos_update.statut if enclos_update.statut is not None else enclos.statut
    
    try:
        db.commit()
        db.refresh(enclos)
        return enclos
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour de l'enclos : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

def delete_enclos(enclos_id: int, db: Session = Depends(get_db)):
    enclos = get_enclos(enclos_id, db)
    if not enclos:
        raise HTTPException(status_code=404, detail=f"Enclos avec l'ID {enclos_id} non trouvé")
    
    try:
        db.delete(enclos)
        db.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression de l'enclos : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

def get_all_enclos(db: Session = Depends(get_db)):
    try:
        logging.info("Récupération de tous les enclos de la base de données")
        enclos_list = db.query(Enclos).all()
        logging.info(f"{len(enclos_list)} enclos récupérés")
        return enclos_list
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des enclos : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur") 