from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Tutor(Base):
    __tablename__ = "tutores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    animais = relationship("Animal", back_populates="tutor")

class Animal(Base):
    __tablename__ = "animais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_animal = Column(String(60), nullable=False)
    especie = Column(String(40), nullable=False)
    raca = Column(String(60), nullable=True)
    peso_kg = Column(Float, nullable=False)
    tutor_id = Column(Integer, ForeignKey("tutores.id"), nullable=False)


    tutor = relationship("Tutor", back_populates="animais")
    atendimentos = relationship("Atendimento", back_populates="animal")

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_atend = Column(String(10), nullable=False)
    motivo = Column(String(200), nullable=False)
    valor_cons = Column(Float, nullable=False)
    animal_id = Column(Integer, ForeignKey("animais.id"), nullable=False)

    animal = relationship("Animal", back_populates="atendimentos")