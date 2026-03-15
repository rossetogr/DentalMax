from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    telefone = Column(String(20))
    email = Column(String(100), unique=True, index=True)
    data_nascimento = Column(DateTime)
    
    # Relacionamento: Um paciente pode ter várias consultas
    consultas = relationship("Consulta", back_populates="paciente")

class Procedimento(Base):
    __tablename__ = "procedimentos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    duracao_minutos = Column(Integer, default=30)
    valor = Column(Numeric(10, 2))

class Consulta(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    procedimento_id = Column(Integer, ForeignKey("procedimentos.id"))
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    observacoes = Column(String(255))

    # Atalhos para acessar os dados relacionados
    paciente = relationship("Paciente", back_populates="consultas")
    procedimento = relationship("Procedimento")