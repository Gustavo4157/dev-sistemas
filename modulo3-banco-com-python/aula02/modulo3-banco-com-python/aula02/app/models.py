from sqlalchemy import Column, Integer, String, Boolean,Float
from app.database import Base

class Departamento(Base):
    __tablename__ = 'departamentos' # nome da tabela no banco

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    sigla = Column(String(10), nullable=False)
    ativo = Column(Boolean, default=True)

    