from http.client import HTTPException
from uuid import UUID
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import models2
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models2.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Lobaev(BaseModel):
    name: str = Field(min_length=1)
    calibr: str = Field(min_length=1, max_lenght=100)
    description: str = Field(min_length=1, max_length=100)
    weight: int = Field(gt=-1, lt=1000000)


@app.get('/')
def read_api(db: Session = Depends(get_db)):
    return db.query(models2.Lobaev).all()


@app.post('/')
def create_lobaev(lobaev: Lobaev, db: Session = Depends(get_db)):
    lobaev_model = models2.Lobaev()

    lobaev_model.name = lobaev.name
    lobaev_model.calibr = lobaev.calibr
    lobaev_model.description = lobaev.description
    lobaev_model.weight = lobaev.weight

    db.add(lobaev_model)
    db.commit()

    return lobaev


@app.put('/{lobaev_id}')
def update_lobaev(lobaev_id: int, lobaev: Lobaev, db: Session = Depends(get_db)):

    lobaev_model = db.query(models2.Lobaev).filter(
        models2.Lobaev.id == lobaev_id).first()
    
    if lobaev_model is None: 
        raise HTTPException(
            status_code=404,
            detail=f"ID {lobaev_id} does not exist"
        )
    
    lobaev_model.name = lobaev.name
    lobaev_model.calibr = lobaev.calibr
    lobaev_model.description = lobaev.description
    lobaev_model.weight = lobaev.weight

    db.add(lobaev_model)
    db.commit()

    return lobaev


@app.delete('/{lobaev_id}')
def delet_lobaev(lobaev_id: int, db: Session = Depends(get_db)):

    book_model = db.query(models2.Lobaev).filter(
        models2.Lobaev.id == lobaev_id).first()
    
    if book_model is None: 
        raise HTTPException(
            status_code=404,
            detail=f"ID {lobaev_id} does not exist"
        )

    db.query(models2.Lobaev).filter(models2.Lobaev.id == lobaev_id).delete()

    db.commit()