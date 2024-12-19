from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.enclos import Enclos
from app.models.comment import Comment
from ..schemas.enclosSchema import EnclosCreate, EnclosUpdate
from ..services.enclosService import (
    retrieve_enclos,
    get_enclos,
    create_enclos,
    update_enclos,
    delete_enclos,
    get_all_enclos
)
from database import get_db

router = APIRouter()

# GET /encloss - Retrieve all encloss
@router.get("/read_all_encloss")
def read_all_encloss(db: Session = Depends(get_db)):
    encloss = get_all_enclos(db)
    if not encloss:
        raise HTTPException(status_code=404, detail="No encloss found")
    return encloss

# GET /enclos/{enclos_id} - Retrieve a enclos by ID
@router.get("/get/{enclos_id}")
def read_enclos_controller(enclos_id: int, db: Session = Depends(get_db)):
    try:
        enclos = get_enclos(enclos_id, db)
        if not enclos:
            raise HTTPException(status_code=404, detail="Enclos not found")
        return enclos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /enclos - Create a new enclos
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_enclos_controller(enclos: EnclosCreate, db: Session = Depends(get_db)):
    try:
        enclos = create_enclos(enclos, db)
        return enclos
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# PUT /enclos/{enclos_id} - Update a enclos
@router.put("/updateEnclos/{enclos_id}", status_code=status.HTTP_200_OK)
def update_enclos_controller(enclos_id: int, enclos_update: EnclosUpdate, db: Session = Depends(get_db)):
    try:
        enclos = update_enclos(enclos_id, enclos_update, db)
        if not enclos:
            raise HTTPException(status_code=404, detail="Enclos not found")
        return enclos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE /enclos/{enclos_id} - Delete a enclos
@router.delete("/{enclos_id}")
def delete_enclos_controller(enclos_id: int, db: Session = Depends(get_db)):
    try:
        enclos = get_enclos(enclos_id, db)
        if not enclos:
            raise HTTPException(status_code=404, detail="Enclos not found")
        response = delete_enclos(enclos_id, db)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to delete enclos")
        return {"message": "Enclos deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/enclos/by_biome/{biome_id}")
async def get_enclos_by_biome(biome_id: int, db: Session = Depends(get_db)):
    # Récupérer les enclos où biome_id correspond à l'ID passé
    enclos = db.query(Enclos).filter(Enclos.biome_id == biome_id).all()
    return enclos


@router.get("/comments/by_enclosure/{enclos_id}")
async def get_comments_by_enclosure(enclos_id: int, db: Session = Depends(get_db)):
    """
    Récupère les commentaires pour un enclos spécifique en fonction de son ID.
    """
    # Récupérer les commentaires où enclos_id correspond à l'ID passé
    comments = db.query(Comment).filter(Comment.enclos_id == enclos_id).all()
    
    if not comments:
        raise HTTPException(status_code=404, detail="Aucun commentaire trouvé pour cet enclos")

    return comments


