from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..models.animal import Animal
from ..schemas.animalSchema import AnimalCreate, AnimalUpdate
from database import get_db
import logging

# Récupérer un animal par son ID
def retrieve_animal(animal_id: int, db: Session = Depends(get_db)):
    return db.query(Animal).filter(Animal.id == animal_id).first()

# Obtenir un animal par son ID
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal non trouvé")
    return animal

# Créer un nouvel animal
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    db_animal = Animal(
        name=animal.name,
        description=animal.description,
        picture=animal.picture,
        enclos_id=animal.enclos_id,
        admin_id=animal.admin_id
    )
    
    try:
        db.add(db_animal)
        db.commit()
        db.refresh(db_animal)
        return db_animal
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'animal : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Mettre à jour un animal
def update_animal(animal_id: int, animal_update: AnimalUpdate, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal avec l'ID {animal_id} non trouvé")
    
    animal.name = animal_update.name if animal_update.name else animal.name
    animal.description = animal_update.description if animal_update.description else animal.description
    animal.picture = animal_update.picture if animal_update.picture else animal.picture
    animal.enclos_id = animal_update.enclos_id if animal_update.enclos_id else animal.enclos_id
    animal.admin_id = animal_update.admin_id if animal_update.admin_id else animal.admin_id
    
    try:
        db.commit()
        db.refresh(animal)
        return animal
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour de l'animal : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Supprimer un animal
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = get_animal(animal_id, db)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal avec l'ID {animal_id} non trouvé")
    
    try:
        db.delete(animal)
        db.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression de l'animal : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Obtenir tous les animaux
def get_all_animals(db: Session = Depends(get_db)):
    try:
        logging.info("Récupération de tous les animaux de la base de données")
        animals_list = db.query(Animal).all()
        logging.info(f"{len(animals_list)} animaux récupérés")
        return animals_list
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des animaux : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
    
def search_animal_and_get_enclos(search_term: str, db: Session = Depends(get_db)):
    try:
        # Recherche l'animal en fonction du nom ou de la description
        animal = db.query(Animal).filter(
            (Animal.name.ilike(f"%{search_term}%")) | 
            (Animal.description.ilike(f"%{search_term}%"))
        ).first()

        if not animal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal non trouvé")
        
        # Vérifie si l'animal a un enclos associé
        if not animal.enclos:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cet animal n'est associé à aucun enclos")
        
        # Retourne l'enclos associé à l'animal
        return animal.enclos

    except HTTPException as http_exc:
        # Cette exception est levée pour des erreurs attendues (par exemple, l'animal n'est pas trouvé)
        raise http_exc
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de l'animal et de l'enclos : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

