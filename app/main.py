from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import router 

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "SFES - Sistema de Fila de Espera do SUS", 
    description = "API de gerenciamento de fila de espera e tempo estimado",
    version = "0.1.0"
)

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "API do SFES funcionando"}