from db.models import Base, engine

# Utworzenie wszystkich tabel wg definicji w db/models.py
Base.metadata.create_all(engine)

print("Tabele zostały utworzone!")