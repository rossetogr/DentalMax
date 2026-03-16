from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List


router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


@router.get("/", response_model=List[schemas.Paciente])
def listar_pacientes(db: Session = Depends(database.get_db)):
    # Busca todos os pacientes no banco
    pacientes = db.query(models.Paciente).all()
    return pacientes


@router.post("/", response_model=schemas.Paciente)
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

@router.put("/{paciente_id}", response_model=schemas.Paciente)
def atualizar_paciente(paciente_id: int, paciente_atualizado: schemas.PacienteCreate, db: Session = Depends(database.get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    # Atualiza os campos
    db_paciente.nome = paciente_atualizado.nome
    db_paciente.email = paciente_atualizado.email
    db_paciente.telefone = paciente_atualizado.telefone
    
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Rotas para Deletar Pacientes, Procedimentos e Consultas
@router.delete("/{paciente_id}")
def deletar_paciente(paciente_id: int, db: Session = Depends(database.get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(paciente)
    db.commit()
    return {"detail": "Paciente deletado com sucesso"}  
