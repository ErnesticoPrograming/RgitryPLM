# modules.py
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)

class Pigeon(Base):
    __tablename__ = "pigeons"
    id = Column(Integer, primary_key=True)
    ring_number = Column(String, unique=True)
    color = Column(String)
    breed = Column(String)
    notes = Column(Text)

def setup_database():
    Base.metadata.create_all(engine)

def add_pigeon(data):
    session = Session()
    pigeon = Pigeon(**data)
    session.add(pigeon)
    session.commit()
    session.close()

def get_all_pigeons():
    session = Session()
    pigeons = session.query(Pigeon).all()
    session.close()
    return pigeons