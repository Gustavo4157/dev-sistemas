from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import LivroModel
from schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.get("/buscar", response_model=List[LivroResponse])
def buscar_livro_por_titulo(titulo: str, db: Session = Depends(get_db)):
    livros = (
        db.query(LivroModel)
        .filter(LivroModel.titulo.ilike(f"%{titulo}%"))
        .all()
    )
    return livros


@router.get("", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(LivroModel).filter(LivroModel.disponivel == True).all()
    return livros


@router.get("/{id}", response_model=LivroResponse)
def buscar_livro_por_id(id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroModel).filter(LivroModel.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )
    return livro

@router.post(
    "",
    response_model=LivroResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    novo_livro = LivroModel(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

@router.patch("/{id}", response_model=LivroResponse)
def atualizar_livro(
    id: int, livro_data: LivroUpdate, db: Session = Depends(get_db)
):
    livro = db.query(LivroModel).filter(LivroModel.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    dados_atualizados = livro_data.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizados.items():
        setattr(livro, chave, valor)

    db.commit()
    db.refresh(livro)
    return livro

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroModel).filter(LivroModel.id == id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado",
        )

    livro.disponivel = False
    db.commit()
    return None