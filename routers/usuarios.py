from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ── Modelos Pydantic ─────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nome:   str
    login:  str
    perfil: str  # "admin" ou "operador"


class UsuarioUpdate(BaseModel):
    nome:   Optional[str] = None
    login:  Optional[str] = None
    perfil: Optional[str] = None


# ── Função auxiliar ──────────────────────────────────────────────────────────

def get_or_404(usuario_id: int, db: Session) -> Usuario:
    # TODO: busque o usuário no banco; se não existir, raise HTTPException 404
    pass


# ── Rotas ────────────────────────────────────────────────────────────────────

@router.get("/")
def listar(db: Session = Depends(get_db)):
    # TODO: retorne todos os usuários
    pass


@router.get("/{usuario_id}")
def buscar(usuario_id: int, db: Session = Depends(get_db)):
    # TODO: use get_or_404
    pass


@router.post("/", status_code=201)
def criar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # TODO: verifique se o login já existe → 409
    # TODO: crie e salve o usuário
    pass


@router.put("/{usuario_id}")
def atualizar(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    # TODO: use get_or_404; atualize apenas os campos enviados
    pass


@router.delete("/{usuario_id}")
def deletar(usuario_id: int, db: Session = Depends(get_db)):
    # TODO: use get_or_404; delete e retorne mensagem de confirmação
    pass
