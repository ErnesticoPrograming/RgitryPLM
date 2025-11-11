from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

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
    captures = relationship("Capture", back_populates="pigeon")

class Capture(Base):
    __tablename__ = "captures"
    id = Column(Integer, primary_key=True)
    pigeon_id = Column(Integer, ForeignKey("pigeons.id"))
    location = Column(String)
    date = Column(String)
    count = Column(Integer)
    pigeon = relationship("Pigeon", back_populates="captures")

class BreedingPair(Base):
    __tablename__ = "breeding_pairs"
    id = Column(Integer, primary_key=True)
    male_id = Column(Integer, ForeignKey("pigeons.id"))
    female_id = Column(Integer, ForeignKey("pigeons.id"))
    male = relationship("Pigeon", foreign_keys=[male_id])
    female = relationship("Pigeon", foreign_keys=[female_id])
    offspring = relationship("Offspring", back_populates="pair")

class Offspring(Base):
    __tablename__ = "offspring"
    id = Column(Integer, primary_key=True)
    ring_number = Column(String, unique=True)
    pair_id = Column(Integer, ForeignKey("breeding_pairs.id"), nullable=True)
    notes = Column(Text)
    pair = relationship("BreedingPair", back_populates="offspring")

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

def update_pigeon(pigeon_id, data):
    session = Session()
    pigeon = session.query(Pigeon).get(pigeon_id)
    if pigeon:
        pigeon.ring_number = data["ring_number"]
        pigeon.color = data["color"]
        pigeon.breed = data["breed"]
        pigeon.notes = data["notes"]
        session.commit()
    session.close()

def delete_pigeon(pigeon_id):
    session = Session()
    pigeon = session.query(Pigeon).get(pigeon_id)
    if pigeon:
        session.delete(pigeon)
        session.commit()
    session.close()

def add_capture(pigeon_id, location, date, count):
    session = Session()
    capture = Capture(pigeon_id=pigeon_id, location=location, date=date, count=count)
    session.add(capture)
    session.commit()
    session.close()

def get_captures_by_pigeon(pigeon_id):
    session = Session()
    captures = session.query(Capture).filter_by(pigeon_id=pigeon_id).all()
    session.close()
    return captures

def add_breeding_pair(male_id, female_id):
    session = Session()
    pair = BreedingPair(male_id=male_id, female_id=female_id)
    session.add(pair)
    session.commit()
    session.close()

def get_all_pairs():
    session = Session()
    pairs = session.query(BreedingPair).all()
    session.close()
    return pairs

def add_offspring(ring_number, pair_id=None, notes=""):
    session = Session()
    offspring = Offspring(ring_number=ring_number, pair_id=pair_id, notes=notes)
    session.add(offspring)
    session.commit()
    session.close()

def get_offspring_by_pair(pair_id):
    session = Session()
    offspring = session.query(Offspring).filter_by(pair_id=pair_id).all()
    session.close()
    return offspring

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_pigeon_pdf(pigeon, captures, filepath):
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Ficha de Paloma: {pigeon.ring_number}")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Color: {pigeon.color}")
    y -= 20
    c.drawString(50, y, f"Raza: {pigeon.breed}")
    y -= 20
    c.drawString(50, y, f"Notas: {pigeon.notes}")
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Historial de Capturas:")
    y -= 25

    c.setFont("Helvetica", 11)
    for cap in captures:
        c.drawString(60, y, f"{cap.date} - {cap.location} ({cap.count} veces)")
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()