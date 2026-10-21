from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Movimentacao, Produto, Usuario

router = APIRouter(prefix="/movimentacoes", tags=["Movimentacoes"])


# ── Modelos Pydantic ─────────────────────────────────────────────────────────

class MovimentacaoCreate(BaseModel):
    tipo:       str    # "entrada" ou "saida"
    quantidade: float
    observacao: Optional[str] = None
    produto_id: int
    usuario_id: int


# ── Rotas ────────────────────────────────────────────────────────────────────

@router.get("/")
def listar(db: Session = Depends(get_db)):
    # TODO: retorne todas as movimentações
    pass


@router.get("/{movimentacao_id}")
def buscar(movimentacao_id: int, db: Session = Depends(get_db)):
    # TODO: busque a movimentação; 404 se não existir
    pass


@router.post("/", status_code=201)
def criar(dados: MovimentacaoCreate, db: Session = Depends(get_db)):
    # TODO 1: verifique se produto_id existe → 404 "Produto não encontrado"
    # TODO 2: verifique se usuario_id existe → 404 "Usuário não encontrado"
    # TODO 3 (DESAFIO): se tipo == "saida", verifique estoque suficiente → 400
    # TODO 4: crie e salve a movimentação
    pass
