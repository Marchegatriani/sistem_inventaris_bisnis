from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import bahan_baku as models_bahan
from schemas import bahan_baku as schemas_bahan
from auth.security import oauth2_scheme

router = APIRouter(
    prefix="/bahan-baku",
    tags=["Manajemen Bahan Baku"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/", response_model=schemas_bahan.BahanBakuResponse, status_code=status.HTTP_201_CREATED)
def create_bahan(bahan: schemas_bahan.BahanBakuCreate, db: Session = Depends(get_db)):
    db_bahan = models_bahan.BahanBaku(**bahan.model_dump())
    db.add(db_bahan)
    db.commit()
    db.refresh(db_bahan)
    return db_bahan

@router.get("/", response_model=List[schemas_bahan.BahanBakuResponse])
def get_all_bahan(db: Session = Depends(get_db)):
    return db.query(models_bahan.BahanBaku).all()