from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Produto

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Modelos Pydantic
class ProdutoCreate(BaseModel):
    nome: str
    unidade: str
    quantidade_estoque: float = 0.0

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    unidade: Optional[str] = None
    quantidade_estoque: Optional[float] = None

# Função auxiliar
def get_or_404(produto_id: int, db: Session) -> Produto:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Rotas
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return db.query(Produto).all()

@router.get("/{produto_id}")
def buscar(produto_id: int, db: Session = Depends(get_db)):
    return get_or_404(produto_id, db)

@router.post("/", status_code=201)
def criar(dados: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(
        nome=dados.nome,
        unidade=dados.unidade,
        quantidade_estoque=dados.quantidade_estoque
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.put("/{produto_id}")
def atualizar(produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = get_or_404(produto_id, db)
    
    dados_dict = dados.model_dump(exclude_unset=True)
    for campo, valor in dados_dict.items():
        setattr(produto, campo, valor)
        
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{produto_id}")
def deletar(produto_id: int, db: Session = Depends(get_db)):
    produto = get_or_404(produto_id, db)
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto removido com sucesso"}