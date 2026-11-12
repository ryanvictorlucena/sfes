from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class PacienteCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: Optional[date] = None
    contato: Optional[str] = None

class TicketCreate(BaseModel):
    unidade_id: int
    paciente_id: int

class TicketPublico(BaseModel):
    id: int
    posicao: int
    iniciais: str
    status: str

class TicketInterno(BaseModel):
    id: int
    unidade_id: int
    paciente_id: int
    status: str
    criado_em: datetime
    chamado_em: Optional[datetime]
    iniciado_em: Optional[datetime]
    finalizado_em: Optional[datetime]

class Config:
    from_attribute = True