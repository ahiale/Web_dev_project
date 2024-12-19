from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..models.comment import Comment
from ..schemas.commentSchema import CommentCreate, CommentUpdate
from database import get_db
import logging

# Récupérer un comment par son ID
def retrieve_comment(comment_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.id == comment_id).first()

# Obtenir un comment par son ID
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment non trouvé")
    return comment

# Créer un nouvel comment
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(
        content=comment.content,
        enclos_id=comment.enclos_id,
        user_id=comment.user_id
    )
    
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'comment : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Mettre à jour un comment
def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment avec l'ID {comment_id} non trouvé")
    
    comment.content = comment_update.content if comment_update.content else comment.content
    
    try:
        db.commit()
        db.refresh(comment)
        return comment
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour de l'comment : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Supprimer un comment
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = get_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment avec l'ID {comment_id} non trouvé")
    
    try:
        db.delete(comment)
        db.commit()
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la suppression de l'comment : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Obtenir tous les animaux
def get_all_comments(db: Session = Depends(get_db)):
    try:
        logging.info("Récupération de tous les animaux de la base de données")
        comments_list = db.query(Comment).all()
        logging.info(f"{len(comments_list)} animaux récupérés")
        return comments_list
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des animaux : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
