from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI(
    title='API de Cadastro -- SENAI',
    description='Primeira API do curso de DS',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    cargo: str
    salario: float
    ativo: bool = True

    @field_validator('salario')
    @classmethod
    def validar_salario(cls, valor: float) -> float:
        if valor <= 0:
            raise ValueError('O salário deve ser maior que zero.')
        return valor


usuarios_db = [
    {'id': 1, 'nome': 'Max Muller', 'cargo': 'DEV', 'salario': 5000.0, 'ativo': True},
    {'id': 2, 'nome': 'Alice Lima', 'cargo': 'Design', 'salario': 4200.0, 'ativo': True},
    {'id': 3, 'nome': 'Carlos Silva', 'cargo': 'QA', 'salario': 3800.0, 'ativo': False},
    {'id': 4, 'nome': 'Diana', 'cargo': 'Gerente', 'salario': 8000.0, 'ativo': True}
]

proximo_id = 5


@app.get('/')
def raiz():
    return {'mensagem': 'API funcionando!', 'versao': '0.1.0'}


@app.get('/status')
def status():
    return {'status': 'online', 'servico': 'API SENAI'}


@app.get('/usuarios/busca')
def buscar_por_nome(nome: str = ''):
    if not nome:
        return usuarios_db
    return [u for u in usuarios_db if nome.lower() in u['nome'].lower()]


@app.get('/usuarios/ativos')
def listar_ativos():
    return [u for u in usuarios_db if u['ativo']]


@app.get('/usuarios/inativos')
def listar_inativos():
    return [u for u in usuarios_db if not u['ativo']]


@app.get('/usuarios/cargo/{cargo}')
def buscar_por_cargo(cargo: str):
    return [u for u in usuarios_db if cargo.lower() in u['cargo'].lower()]


@app.get('/info')
def info_geral():
    return {
        'total_usuarios': len(usuarios_db),
        'ativos': sum(1 for u in usuarios_db if u['ativo']),
        'inativos': sum(1 for u in usuarios_db if not u['ativo'])
    }


@app.get('/usuarios')
def listar_usuarios():
    return usuarios_db


@app.get('/usuarios/{usuario_id}')
def buscar_usuario(usuario_id: int):
    for usuario in usuarios_db:
        if usuario['id'] == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail='Usuário não encontrado')


@app.post('/usuarios', status_code=201)
def criar_usuario(usuario: Usuario):
    global proximo_id
    novo = usuario.model_dump()
    novo['id'] = proximo_id
    proximo_id += 1
    usuarios_db.append(novo)
    return novo