from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Verbindung zur Datenbank herstellen
engine = db.create_engine('sqlite:///scannerMarket.db', echo=True)  # Passen Sie die Verbindungsdaten an

Base = db.declarative_base()

class Nutzer(Base):
    __tablename__ = 'nutzer'

    ID = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(45))
    nachname = db.Column(db.String(45))
    geb_datum = db.Column(db.Date)
    email = db.Column(db.String(45), nullable=False, unique=True)
    passwort = db.Column(db.String(45), nullable=False)
    kundenkarte = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    newsletter = db.Column(db.Boolean)

class Bezahlmöglichkeiten(Base):
    __tablename__ = 'bezahlmöglichkeiten'

    ID = db.Column(db.Integer, primary_key=True)
    methode = db.Column(db.String(45))

class Bezahlung(Base):
    __tablename__ = 'bezahlung'

    nutzer_ID = db.Column(db.Integer, db.ForeignKey('nutzer.ID'), primary_key=True)
    bezahlmöglichkeiten_ID = db.Column(db.Integer, db.ForeignKey('bezahlmöglichkeiten.ID'), primary_key=True)
    konto_email = db.Column(db.String(45))
    karten_nr = db.Column(db.String(45))

    nutzer = relationship("Nutzer", backref="bezahlungen")  # backref wird verwendet, um eine bidirektionale Beziehung zu ermöglichen
    bezahlmöglichkeiten = relationship("Bezahlmöglichkeiten", backref="bezahlungen")

class Produktkategorien(Base):
    __tablename__ = 'produktkategorien'

    ID = db.Column(db.Integer, primary_key=True)
    kategorie = db.Column(db.String(45))

class Produkte(Base):
    __tablename__ = 'produkte'

    ID = db.Column(db.Integer, primary_key=True)
    hersteller = db.Column(db.String(45))
    produkt_name = db.Column(db.String(45))
    gewicht_volumen = db.Column(db.String(45))
    ean = db.Column(db.Integer)
    preis = db.Column(db.Float)
    bild = db.Column(db.String)  # BLOB-Typ wird nicht direkt unterstützt, kann jedoch als String behandelt werden
    produktkategorien_ID = db.Column(db.Integer, db.ForeignKey('produktkategorien.ID'))

    produktkategorien = relationship("Produktkategorien")

class Einkauf(Base):
    __tablename__ = 'einkauf'

    ID = db.Column(db.Integer, primary_key=True)
    nutzer_ID = db.Column(db.Integer, db.ForeignKey('nutzer.ID'))
    zeitstempel_start = db.Column(db.DateTime)
    zeitstempel_ende = db.Column(db.DateTime)

    nutzer = relationship("Nutzer")

class Warenkorb(Base):
    __tablename__ = 'warenkorb'

    einkauf_ID = db.Column(db.Integer, db.ForeignKey('einkauf.ID'), primary_key=True)
    produkte_ID = db.Column(db.Integer, db.ForeignKey('produkte.ID'), primary_key=True)
    anzahl = db.Column(db.Integer)

    einkauf = relationship("Einkauf")
    produkte = relationship("Produkte")

# Tabellen erstellen
Base.metadata.create_all(engine)
