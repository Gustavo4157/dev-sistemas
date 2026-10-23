# # Criar o banco e tabela via python puro
# import sqlite3

# # Conectar ao banco (criar o arquivo se não existir)
# conn = sqlite3.connect('funcionarios.db')
# cursor = conn.cursor()

# #Criar tabela departamentos
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS  departamentos (
#     id INTEGER PRIMARY KEY AUTOINCREMENT, 
#     nome text not null,
#     sigla TEXT NOT NULL,
#     ativo INTEGER DEFAULT 1
#     )
# ''')

# # Inserir departamentos
# cursor.executemany(
#     'INSERT INTO departamentos (nome, sigla) VALUES (?, ?)',
#     [
#         ('Tecnologia da Informação', 'TI'),
#         ('Recursos Humanos', 'RH'),
#         ('Financeiro', 'FIN'),
#         ('Comercial', 'COM')
#     ]
# )
# conn.commit()

# # Consultar
# cursor.execute('SELECT * FROM departamentos')
# print('Departamentos:')
# for linha in cursor.fetchall():
#     print(f' id={linha[0]} nome={linha[1]} sigla={linha[2]}')

#     conn.close()
#     print('Banco criado com sucesso!')

# conn.close()

from sqlalchemy import Column, Integer, String, Boolean, text
from app.database import engine, Base, SessionLocal

# Definir o modelo (tabela) diretamete aqui por enquanto
# Na próxima aula colocaremos no app/models.py
class Departamento(Base):
    __tablename__ = 'departamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    sigla = Column(String(10), nullable=False)
    ativo = Column(Boolean, default=True)
    

# Criar a tabela no banco~
#   rwBase. metadata.create_all(bind=engine)
print('Tabela criada!')

# Inserir dados via sessão
db = SessionLocal()
try:

    # Verificar se já tem dados
    if db.query(Departamento).count() == 0:
        db.add_all([
        Departamento(nome='Tecnologia da Informação', sigla='TI'),
        Departamento(nome='Recursos Humanos', sigla='RH'),
        Departamento(nome='Comercial', sigla='COM'),
        Departamento(nome='Financeiro', sigla='FIN')
    ])
    db.commit()
    print('Dados inseridos')

    # Consultar via SQLAlchemy
    deptos = db.query(Departamento).order_by(Departamento.nome).all()
    print(f'\n{len(deptos)} departamentos no banco')
    for d in deptos:
        print(f'{d.id}: {d.nome} ({d.sigla})')
finally:
    db.close()  