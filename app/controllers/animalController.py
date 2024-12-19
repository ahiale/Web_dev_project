from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.models.enclos import Enclos
from ..schemas.animalSchema import AnimalCreate, AnimalUpdate
from ..services.animalService import (
    create_animal,
    get_animal,
    get_all_animals,
    search_animal_and_get_enclos,
    update_animal,
    delete_animal
)
from database import get_db

router = APIRouter()

# GET /animals - Retrieve all animals
@router.get("/animals", status_code=status.HTTP_200_OK)
def read_all_animals(db: Session = Depends(get_db)):
    try:
        animals_list = get_all_animals(db)
        if not animals_list:
            raise HTTPException(status_code=404, detail="No animals found")
        return animals_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET /animals/{animal_id} - Retrieve an animal by ID
@router.get("/animals/{animal_id}", status_code=status.HTTP_200_OK)
def read_animal(animal_id: int, db: Session = Depends(get_db)):
    try:
        animal = get_animal(animal_id, db)
        return animal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /animals - Create a new animal
@router.post("/animals", status_code=status.HTTP_201_CREATED)
def create_animal_controller(animal: AnimalCreate, db: Session = Depends(get_db)):
    try:
        new_animal = create_animal(animal, db)
        return new_animal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT /animals/{animal_id} - Update an animal
@router.put("/animals/{animal_id}", status_code=status.HTTP_200_OK)
def update_animal_controller(animal_id: int, animal_update: AnimalUpdate, db: Session = Depends(get_db)):
    try:
        updated_animal = update_animal(animal_id, animal_update, db)
        return updated_animal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE /animals/{animal_id} - Delete an animal
@router.delete("/animals/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal_controller(animal_id: int, db: Session = Depends(get_db)):
    try:
        delete_animal(animal_id, db)
        return {"message": "Animal deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/search-animal-enclos/{search_term}")
def search_animal_enclos(search_term: str, db: Session = Depends(get_db)):
    enclos = search_animal_and_get_enclos(search_term, db)
    return enclos

@router.get("/animals/by_enclos/{enclos_id}")
async def get_animal_by_enclos(enclos_id: int, db: Session = Depends(get_db)):
    # Récupérer les enclos où biome_id correspond à l'ID passé
    animal = db.query(Animal).filter(Animal.enclos_id == enclos_id).all()
    return animal



@router.get("/enclos/by_animal/{animal_name}")
async def get_enclos_by_animal(animal_name: str, db: Session = Depends(get_db)):
    # Rechercher les enclos contenant des animaux correspondant au nom donné
    enclos_with_animal = (
        db.query(Enclos)
        .join(Animal, Enclos.id == Animal.enclos_id)
        .filter(Animal.name.ilike(f"%{animal_name}%"))  # Recherche insensible à la casse
        .all()
    )

    # Vérifier si des enclos ont été trouvés
    if not enclos_with_animal:
        return {"message": f"Aucun enclos trouvé pour l'animal '{animal_name}'", "status": 404}

    # Construire la réponse
    return [
        {
            "id": enclos.id,
            "name": enclos.name,
            "statut": enclos.statut,
            "heuresD": enclos.heuresD.isoformat() if enclos.heuresD else None,
            "heuresF": enclos.heuresF.isoformat() if enclos.heuresF else None,
        }
        for enclos in enclos_with_animal
    ]
