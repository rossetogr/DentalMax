from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List
from datetime import timedelta
from datetime import date, datetime, time # Adicione 'time' e 'date' aos imports
from sqlalchemy import and_

router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)

@router.get("/", response_model=List[schemas.Consulta])
def listar_consultas(db: Session = Depends(database.get_db)):
    # Busca todas as consultas no banco
    consultas = db.query(models.Consulta).all()
    return consultas

# Rota para Agendar Consulta com Validação de Horário
@router.post("/", response_model=schemas.Consulta)
def agendar_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(database.get_db)):
    # 1. Busca o procedimento para saber a duração
    proc = db.query(models.Procedimento).filter(models.Procedimento.id == consulta.procedimento_id).first()
    if not proc:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")

    # 2. Calcula o fim da consulta
    data_fim = consulta.data_inicio + timedelta(minutes=proc.duracao_minutos)

    # 3. VERIFICAÇÃO DE CONFLITO (A Inteligência)
    # Procura consultas que começam antes do fim desta E terminam depois do início desta
    conflito = db.query(models.Consulta).filter(
        models.Consulta.data_inicio < data_fim,
        models.Consulta.data_fim > consulta.data_inicio
    ).first()

    if conflito:
        raise HTTPException(status_code=400, detail="Horário já ocupado por outra consulta")

    # 4. Salva a consulta
    nova_consulta = models.Consulta(
        **consulta.model_dump(),
        data_fim=data_fim
    )
    db.add(nova_consulta)
    db.commit()
    db.refresh(nova_consulta)
    return nova_consulta

@router.delete("/{consulta_id}")
def deletar_consulta(consulta_id: int, db: Session = Depends(database.get_db)):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    db.delete(consulta)
    db.commit()
    return {"detail": "Consulta deletada com sucesso"}

# ... outras rotas ...

@router.get("/timeline/{data_escolhida}", response_model=List[schemas.Consulta])
def buscar_agenda_do_dia(data_escolhida: date, db: Session = Depends(database.get_db)):
    """
    Retorna todas as consultas de um dia específico, ordenadas por horário.
    Formato da data: AAAA-MM-DD (Ex: 2026-03-15)
    """
    # Define o início do dia (00:00:00) e o fim do dia (23:59:59)
    inicio_dia = datetime.combine(data_escolhida, time.min)
    fim_dia = datetime.combine(data_escolhida, time.max)

    # Busca no banco consultas que iniciam dentro desse intervalo
    consultas = db.query(models.Consulta).filter(
        models.Consulta.data_inicio >= inicio_dia,
        models.Consulta.data_inicio <= fim_dia
    ).order_by(models.Consulta.data_inicio).all()
    
    return consultas