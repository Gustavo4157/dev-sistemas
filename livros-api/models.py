from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from database import Base


class LivroModel(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    ano_publicacao = Column(Integer, nullable=True)
    disponivel = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)