from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Modelos Pydantic
class UsuarioCreate(BaseModel):
    nome: str
    login: str
    perfil: str  # "admin" ou "operador"

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    login: Optional[str] = None
    perfil: Optional[str] = None

# Função auxiliar
def get_or_404(usuario_id: int, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# Rotas
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/{usuario_id}")
def buscar(usuario_id: int, db: Session = Depends(get_db)):
    return get_or_404(usuario_id, db)

@router.post("/", status_code=201)
def criar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.login == dados.login).first()
    if usuario_existente:
        raise HTTPException(status_code=409, detail="Login já cadastrado")
    
    novo_usuario = Usuario(
        nome=dados.nome,
        login=dados.login,
        perfil=dados.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.put("/{usuario_id}")
def atualizar(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = get_or_404(usuario_id, db)
    
    dados_dict = dados.model_dump(exclude_unset=True)
    for campo, valor in dados_dict.items():
        setattr(usuario, campo, valor)
        
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}")
def deletar(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_or_404(usuario_id, db)
    db.delete(usuario)
    db.commit()
    return {"mensagem": "Usuário removido com sucesso"}