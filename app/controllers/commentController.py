from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.commentSchema import CommentBase, CommentCreate, CommentUpdate
from app.services.commentService import create_comment, delete_comment, get_comment, get_all_comments, update_comment

from database import get_db
router = APIRouter()

# GET /Comments - Retrieve all Comments
@router.get("/Comments", status_code=status.HTTP_200_OK)
def read_all_Comments(db: Session = Depends(get_db)):
    try:
        Comments_list = get_all_comments(db)
        if not Comments_list:
            raise HTTPException(status_code=404, detail="No Comments found")
        return Comments_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET /Comments/{Comment_id} - Retrieve an Comment by ID
@router.get("/Comments/{Comment_id}", status_code=status.HTTP_200_OK)
def read_Comment(Comment_id: int, db: Session = Depends(get_db)):
    try:
        Comment = get_comment(Comment_id, db)
        return Comment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /Comments - Create a new Comment
@router.post("/Comments", status_code=status.HTTP_201_CREATED)
def create_Comment_controller(Comment: CommentCreate, db: Session = Depends(get_db)):
    try:
        new_Comment = create_comment(Comment, db)
        return new_Comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT /Comments/{Comment_id} - Update an Comment
@router.put("/Comments/{Comment_id}", status_code=status.HTTP_200_OK)
def update_Comment_controller(Comment_id: int, Comment_update: CommentUpdate, db: Session = Depends(get_db)):
    try:
        updated_Comment = update_comment(Comment_id, Comment_update, db)
        return updated_Comment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE /Comments/{Comment_id} - Delete an Comment
@router.delete("/Comments/{Comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Comment_controller(Comment_id: int, db: Session = Depends(get_db)):
    try:
        delete_comment(Comment_id, db)
        return {"message": "Comment deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

