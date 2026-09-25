from app.database import SessionLocal
from app.models import Aluno, Curso


def popular_banco():
    db = SessionLocal()
    try:
        if db.query(Curso).count() > 0 or db.query(Aluno).count() > 0:
            print("Banco já populado. Pulando...")
            return

        cursos = [
            Curso(nome="Python para Beginners", duracao=40, ativo=True),
            Curso(nome="Desenvolvimento Web com FastAPI", duracao=60, ativo=True),
            Curso(nome="Banco de Dados e SQLAlchemy", duracao=30, ativo=True),
        ]
        db.add_all(cursos)
        
        alunos = [
            Aluno(
                nome="Ana Silva",
                email="ana.silva@email.com",
                matricula="2026001",
                ativo=True,
            ),
            Aluno(
                nome="Carlos Oliveira",
                email="carlos.o@email.com",
                matricula="2026002",
                ativo=True,
            ),
            Aluno(
                nome="Mariana Souza",
                email="mariana.s@email.com",
                matricula="2026003",
                ativo=True,
            ),
            Aluno(
                nome="João Santos",
                email="joao.s@email.com",
                matricula="2026004",
                ativo=True,
            ),
        ]
        db.add_all(alunos)

        db.commit()
        print("Banco populado com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao popular o banco: {e}")
    finally:
        db.close()