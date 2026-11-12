from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Unidade(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String, nullable = False)
    endereco = Column(String)

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String, nullable = False)
    cpf = Column(String, unique = True, index = True)
    data_nascimento = Column(Date)
    contato = Column(String)

class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key = True, index = True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable = False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable = False)
    status = Column(String, default = "AGUARDANDO", nullable = False)
    criado_em = Column(DateTime, default = datetime.utcnow, nullable = False)
    chamado_em = Column(DateTime, nullable = True)
    iniciado_em = Column(DateTime, nullable = True)
    finalizado_em = Column(DateTime, nullable = True)
    