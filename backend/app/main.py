from fastapi import FastAPI
from .database import engine
from . import models
from .routers import pacientes, procedimentos, consultas # Importa o arquivo que você criou

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DentalMax API")

# Aqui está a mágica: Inclui as rotas do arquivo de pacientes
app.include_router(pacientes.router)
app.include_router(procedimentos.router)
app.include_router(consultas.router)

@app.get("/")
def home():
    return {"message": "DentalMax API rodando!"}