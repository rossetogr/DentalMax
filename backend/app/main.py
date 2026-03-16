from fastapi import FastAPI
from .database import engine
from . import models
from .routers import pacientes, procedimentos, consultas
from fastapi.middleware.cors import CORSMiddleware

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DentalMax API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Aqui está a mágica: Inclui as rotas do arquivo de pacientes
app.include_router(pacientes.router)
app.include_router(procedimentos.router)
app.include_router(consultas.router)

@app.get("/")
def home():
    return {"message": "DentalMax API rodando!"}