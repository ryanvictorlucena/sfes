from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

def obter_iniciais(nome: str) -> str:
    partes = nome.split()
    if len(partes) == 1:
        return partes[0][:2].upper()
    return (partes[0][0] + partes[-1][0]).upper()

@router.post("/unidades")
def criar_unidade(nome: str, endereco: str, db: schemas = Depends(get_db)):
    db_unidade = models.Unidade(nome = nome, endereco = endereco)
    db.add(db_unidade)
    db.commit()
    db.refresh(db_unidade)
    return db_unidade

@router.post("/pacientes", response_model = schemas.PacienteCreate)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.post("/tickets", response_model = schemas.TicketInterno)
def criar_ticket(payload: schemas.TicketCreate, db: Session = Depends(get_db)):
    novo_ticket = models.Ticket(
        unidade_id = payload.unidade_id,
        paciente_id = payload.paciente_id,
        status = "AGUARDANDO"
    )
    db.add(novo_ticket)
    db.commit()
    db.refresh(novo_ticket)
    return novo_ticket

@router.get("/filas/{unidade_id}", response_model = List[schemas.TicketPublico])
def listar_fila(unidade_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.unidade_id == unidade_id, 
        models.Ticket.status == "AGUARDANDO"
    ).order_by(models.Ticket.criado_em).all()

    resultado = []
    for index, ticket in enumerate(ticket):
        paciente = db.query(models.Paciente).filter(models.Paciente.id == ticket.paciente_id).first()
        resultado.append({
            "id": ticket.id,
            "posicao": index + 1,
            "iniciais": obter_iniciais(paciente.nome) if paciente else "??",
            "status": ticket.status
        })
    return resultado

@router.get("/painel/{unidade_id}")
def listar_fila_painel(unidade_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.unidade_id == unidade_id,
        models.Ticket.status.in_(["AGUARDANDO", "CHAMADO", "EM_ATENDIMENTO"])
    ).order_by(models.Ticket.criado_em).all()

    resultado = []
    for tickets in ticket:
        paciente = db.query(models.Paciente).filter(
            models.Paciente.id == tickets.paciente_id).first()
        resultado.append({
            "id": tickets.id,
            "nome_completo": paciente.nome,
            "paciente_id": paciente.id,
            "status": tickets.status
        })
    return resultado

    @router.post("/tickets/{ticket_id}/chamar", response_model = schemas.TicketInterno)
    def chamar_ticket(ticket_id: int, db: Session = Depends(get_db)):
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code = 404, detail = "Ticket não encontrado!")
        if ticket.status != "AGUARDANDO":
            raise HTTPException(status_code = 400, detail = "Ticket não está aguardando!")

        ticket.status = "CHAMADO"
        ticket.chamado_em = datetime.utcnow()
        db.commit()
        db.refresh(ticket)
        return ticket

    @router.post("/tickets/{ticket_id}/iniciar", response_model = schemas.TicketInterno)
    def iniciar_atendimento(ticket_id: int, db: Session = Depends(get_db)):
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code = 404, detail = "Ticket não encontrado!")

        ticket.status = "EM_ATENDIMENTO"
        ticket.iniciado_em: datetime.utcnow()
        db.commit()
        db.refresh(ticket)
        return ticket

    @router.post("/tickets/{ticket_id}/finalizar", response_model = schemas.TicketInterno)
    def finalizar_atendimento(ticket_id: int, db: Session = Depends(get_db)):
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code = 404, detail = "Ticket não encontrado!")

        ticket.status = "ATENDIDO"
        ticket.finalizado_em = datetime.utcnow()
        db.commit()
        db.refresh(ticket)
        return ticket