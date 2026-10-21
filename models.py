from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


# TODO: Implemente os 3 modelos abaixo


# Tabela: usuarios
# Campos: id (PK), nome (String 100), login (String 50, unique), perfil (String 20)
class Usuario(Base):
    __tablename__ = "usuarios"

    # TODO: adicione os campos aqui
    pass


# Tabela: produtos
# Campos: id (PK), nome (String 100), unidade (String 20),
#         quantidade_estoque (Float, default=0.0)
class Produto(Base):
    __tablename__ = "produtos"

    # TODO: adicione os campos aqui
    pass


# Tabela: movimentacoes
# Campos: id (PK), tipo (String 10), quantidade (Float),
#         observacao (String 300, nullable), produto_id (FK), usuario_id (FK)
class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    # TODO: adicione os campos aqui
    pass
