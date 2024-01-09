from typing import List
from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, utils, database
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    # hash password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id=} was not exist")

    return user


@router.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.put("/users/{id}", response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    updated_user = db.query(models.User).filter(models.User.id == id)

    if not updated_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id=} was not exist")

    # hash password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    updated_user.update(user.model_dump(), synchronize_session=False)
    db.commit()

    return updated_user.first()


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id=} was not exist")

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
