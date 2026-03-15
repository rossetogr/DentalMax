from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List


router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


@router.get("/pacientes/", response_model=List[schemas.Paciente])
def listar_pacientes(db: Session = Depends(database.get_db)):
    # Busca todos os pacientes no banco
    pacientes = db.query(models.Paciente).all()
    return pacientes


@router.post("/pacientes/", response_model=schemas.Paciente)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(database.get_db)):
    # 1. Verifica se o e-mail já existe
    db_paciente = db.query(models.Paciente).filter(models.Paciente.email == paciente.email).first()
    if db_paciente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # 2. Transforma o Schema em Model
    novo_paciente = models.Paciente(**paciente.model_dump())
    
    # 3. Salva no banco
    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)
    
    return novo_paciente

# Rotas para Deletar Pacientes, Procedimentos e Consultas
@router.delete("/pacientes/{paciente_id}")
def deletar_paciente(paciente_id: int, db: Session = Depends(database.get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(paciente)
    db.commit()
    return {"detail": "Paciente deletado com sucesso"}  
