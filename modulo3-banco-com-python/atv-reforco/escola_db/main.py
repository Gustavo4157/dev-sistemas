from app.database import Base, engine
from app.models import Aluno, Curso  
from app.seed import popular_banco

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    popular_banco()