from datetime import datetime
from app.database import engine, Base, SessionLocal
from app.crud import inserir_tutor, inserir_animal, inserir_atendimento

def main():
    Base.metadata.create_all(bind=engine)

    # Abrir sessão
    db = SessionLocal()

    try:
        
        data_hoje = datetime.now().strftime("%d/%m/%Y")

     
        tutor1 = inserir_tutor(db, nome_completo="Kevin Campos", telefone="61999998888", email="kevin@email.com")
        print(f"Tutor inserido: {tutor1.nome_completo} (id={tutor1.id})")

        tutor2 = inserir_tutor(db, nome_completo="Gustavo Santos", telefone="61977778888", email="gustavo@email.com")
        print(f"Tutor inserido: {tutor2.nome_completo} (id={tutor2.id})")

       
        animal1 = inserir_animal(db, nome_animal="snoopy", especie="cão", raca="Pastor Alemão", peso_kg=28.5, tutor_id=tutor1.id)
        print(f"Animal inserido: {animal1.nome_animal} - {animal1.especie}")

        animal2 = inserir_animal(db, nome_animal="Fred", especie="gato", raca="Egípcio", peso_kg=4.2, tutor_id=tutor1.id)
        print(f"Animal inserido: {animal2.nome_animal} - {animal2.especie}")

        animal3 = inserir_animal(db, nome_animal="Bobby", especie="ave", raca="Calopsita", peso_kg=0.4, tutor_id=tutor2.id)
        print(f"Animal inserido: {animal3.nome_animal} - {animal3.especie}")

        
        atend1 = inserir_atendimento(db, data_atend=data_hoje, motivo="Vacina anual V8", valor_cons=150.00, animal_id=animal1.id)
        print(f"Atendimento: {atend1.motivo} | R$ {atend1.valor_cons:.2f}")

        atend2 = inserir_atendimento(db, data_atend=data_hoje, motivo="Consulta de rotina", valor_cons=120.00, animal_id=animal2.id)
        print(f"Atendimento: {atend2.motivo} | R$ {atend2.valor_cons:.2f}")

        atend3 = inserir_atendimento(db, data_atend=data_hoje, motivo="Corte de unhas e bico", valor_cons=80.00, animal_id=animal3.id)
        print(f"Atendimento: {atend3.motivo} | R$ {atend3.valor_cons:.2f}")

    finally:
        db.close()

if __name__ == "__main__":
    main()