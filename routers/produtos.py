from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Produto

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# ── Modelos Pydantic ─────────────────────────────────────────────────────────

class ProdutoCreate(BaseModel):
    nome:               str
    unidade:            str
    quantidade_estoque: float = 0.0


class ProdutoUpdate(BaseModel):
    nome:               Optional[str]   = None
    unidade:            Optional[str]   = None
    quantidade_estoque: Optional[float] = None


# ── Função auxiliar ──────────────────────────────────────────────────────────

def get_or_404(produto_id: int, db: Session) -> Produto:
    # TODO: busque o produto no banco; se não existir, raise HTTPException 404
    pass


# ── Rotas ────────────────────────────────────────────────────────────────────

@router.get("/")
def listar(db: Session = Depends(get_db)):
    # TODO: retorne todos os produtos
    pass


@router.get("/{produto_id}")
def buscar(produto_id: int, db: Session = Depends(get_db)):
    # TODO: use get_or_404
    pass


@router.post("/", status_code=201)
def criar(dados: ProdutoCreate, db: Session = Depends(get_db)):
    # TODO: crie e salve o produto
    pass


@router.put("/{produto_id}")
def atualizar(produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    # TODO: use get_or_404; atualize apenas os campos enviados
    pass


@router.delete("/{produto_id}")
def deletar(produto_id: int, db: Session = Depends(get_db)):
    # TODO: use get_or_404; delete e retorne mensagem de confirmação
    pass
