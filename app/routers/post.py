from typing import List
from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    posts_querry = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return posts_querry


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perfom request action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id == id)

    post = post_querry.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perfom request action")

    post_querry.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id == id)

    post = post_querry.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id=} was not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perfom request action")

    post_querry.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post
