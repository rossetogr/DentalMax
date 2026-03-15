from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from datetime import datetime

# Base comum para leitura e escrita
class PacienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: EmailStr
    data_nascimento: Optional[date] = None

# Dados necessários para CRIAR um paciente (o que o usuário envia)
class PacienteCreate(PacienteBase):
    pass

# Dados que a API DEVOLVE (inclui o ID que o banco gerou)
class Paciente(PacienteBase):
    id: int

    class Config:
        from_attributes = True # Permite que o Pydantic leia modelos do SQLAlchemy

# --- PROCEDIMENTOS ---
class ProcedimentoBase(BaseModel):
    nome: str
    duracao_minutos: int
    valor: float

class ProcedimentoCreate(ProcedimentoBase):
    pass

class Procedimento(ProcedimentoBase):
    id: int
    class Config:
        from_attributes = True

# --- CONSULTAS ---
class ConsultaBase(BaseModel):
    paciente_id: int
    procedimento_id: int
    data_inicio: datetime
    observacoes: Optional[str] = None

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id: int
    data_fim: datetime # O backend vai calcular isso automaticamente
    class Config:
        from_attributes = True