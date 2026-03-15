from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Pega a URL do banco das variáveis de ambiente do Docker
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:root_password@db/odonto_db")

# O engine é o "motor" que conversa com o MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criador de sessões (cada clique no site abrirá uma sessão)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para nossos modelos (tabelas) herdarem
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()