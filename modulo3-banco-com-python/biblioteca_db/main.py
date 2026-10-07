from app.database import engine, SessionLocal, Base
from app import models


def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")


def popular_tabelas():
    with SessionLocal() as db:
        # Evita duplicar dados se o arquivo for executado mais de uma vez
        if db.query(models.Genero).first():
            print("Banco já populado. Nada a inserir.")
            return

        # 1º Gêneros
        ficcao = models.Genero(nome="Ficção")
        romance = models.Genero(nome="Romance")
        fantasia = models.Genero(nome="Fantasia")
        db.add_all([ficcao, romance, fantasia])
        db.commit()
        print("Gêneros inseridos.")

        # 2º Autores
        machado = models.Autor(nome="Machado de Assis", nacionalidade="Brasileira")
        orwell = models.Autor(nome="George Orwell", nacionalidade="Britânica")
        tolkien = models.Autor(nome="J.R.R. Tolkien", nacionalidade="Britânica")
        clarice = models.Autor(nome="Clarice Lispector", nacionalidade="Brasileira")
        db.add_all([machado, orwell, tolkien, clarice])
        db.commit()
        print("Autores inseridos.")

        # 3º Livros (dependem dos ids de gêneros e autores)
        livros = [
            models.Livro(titulo="Dom Casmurro", ano_publicacao=1899,
                         genero_id=romance.id, autor_id=machado.id),
            models.Livro(titulo="Memórias Póstumas de Brás Cubas", ano_publicacao=1881,
                         genero_id=romance.id, autor_id=machado.id),
            models.Livro(titulo="1984", ano_publicacao=1949,
                         genero_id=ficcao.id, autor_id=orwell.id),
            models.Livro(titulo="A Revolução dos Bichos", ano_publicacao=1945,
                         genero_id=ficcao.id, autor_id=orwell.id, disponivel=False),
            models.Livro(titulo="O Senhor dos Anéis", ano_publicacao=1954,
                         genero_id=fantasia.id, autor_id=tolkien.id),
            models.Livro(titulo="A Hora da Estrela", ano_publicacao=1977,
                         genero_id=romance.id, autor_id=clarice.id),
        ]
        db.add_all(livros)
        db.commit()
        print("Livros inseridos.")


if __name__ == "__main__":
    criar_tabelas()
    popular_tabelas()