from app.database import engine, Base
from app import models #importar para registrar os modelos na Base

Base.metadata.create_all(bind=engine)
print('Tabelas criadas')