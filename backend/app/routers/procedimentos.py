from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List

router = APIRouter(
    prefix="/procedimentos",
    tags=["Procedimentos"]
)


@router.get("/", response_model=List[schemas.Procedimento])
def listar_procedimentos(db: Session = Depends(database.get_db)):
    # Busca todos os procedimentos no banco
    procedimentos = db.query(models.Procedimento).all()
    return procedimentos

@router.post("/", response_model=schemas.Procedimento)
def criar_procedimento(procedimento: schemas.ProcedimentoCreate, db: Session = Depends(database.get_db)):
    novo_proc = models.Procedimento(**procedimento.model_dump())
    db.add(novo_proc)
    db.commit()
    db.refresh(novo_proc)
    return novo_proc

@router.delete("/{procedimento_id}")
def deletar_procedimento(procedimento_id: int, db: Session = Depends(database.get_db)):
    procedimento = db.query(models.Procedimento).filter(models.Procedimento.id == procedimento_id).first()
    if not procedimento:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    
    db.delete(procedimento)
    db.commit()
    return {"detail": "Procedimento deletado com sucesso"}