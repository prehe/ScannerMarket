from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Verbindung zur Datenbank herstellen
engine = db.create_engine('sqlite:///scannerMarket.db', echo=True)  # Passen Sie die Verbindungsdaten an

class Nutzer(db.Model):
    __tablename__ = 'nutzer'

    ID = db.Column(db.Integer, primary_key=True)
    Vorname = db.Column(db.String(45))
    Nachname = db.Column(db.String(45))
    Geburtsdatum = db.Column(db.Date)
    Email = db.Column(db.String(45), nullable=False, unique=True)
    Passwort = db.Column(db.String(45), nullable=False)
    Kundenkarte = db.Column(db.Boolean)
    Admin = db.Column(db.Boolean)
    Newsletter = db.Column(db.Boolean)
    Registriert_am = db.Column(db.DateTime)

class Bezahlmöglichkeiten(db.Model):
    __tablename__ = 'bezahlmöglichkeiten'

    ID = db.Column(db.Integer, primary_key=True)
    Methode = db.Column(db.String(45))

class Bezahlung(db.Model):
    __tablename__ = 'bezahlung'

    Nutzer_ID = db.Column(db.Integer, db.ForeignKey('nutzer.ID'), primary_key=True)
    Bezahlmöglichkeiten_ID = db.Column(db.Integer, db.ForeignKey('bezahlmöglichkeiten.ID'), primary_key=True)
    PP_Email = db.Column(db.String(45))
    Karten_Nr = db.Column(db.String(45))
    Karte_Gültingkeitsdatum = db.Column(db.DateTime)
    Karte_Prüfnummer = db.Column(db.Integer)

    nutzer = relationship("Nutzer")  # backref wird verwendet, um eine bidirektionale Beziehung zu ermöglichen
    bezahlmöglichkeiten = relationship("Bezahlmöglichkeiten")

class Produktkategorien(db.Model):
    __tablename__ = 'produktkategorien'

    ID = db.Column(db.Integer, primary_key=True)
    Kategorie = db.Column(db.String(45))

class Produkte(db.Model):
    __tablename__ = 'produkte'

    ID = db.Column(db.Integer, primary_key=True)
    Hersteller = db.Column(db.String(45))
    Name = db.Column(db.String(45))
    Gewicht_Volumen = db.Column(db.String(45))
    EAN = db.Column(db.Integer)
    Preis = db.Column(db.Float)
    Bild = db.Column(db.String)  
    Kategorie_ID = db.Column(db.Integer, db.ForeignKey('produktkategorien.ID'))

    produktkategorien = relationship("Produktkategorien")

class Einkauf(db.Model):
    __tablename__ = 'einkauf'

    ID = db.Column(db.Integer, primary_key=True)
    Nutzer_ID = db.Column(db.Integer, db.ForeignKey('nutzer.ID'))
    Zeitstempel_start = db.Column(db.DateTime)
    Zeitstempel_ende = db.Column(db.DateTime)

    nutzer = relationship("Nutzer")

class Warenkorb(db.Model):
    __tablename__ = 'warenkorb'

    Einkauf_ID = db.Column(db.Integer, db.ForeignKey('einkauf.ID'), primary_key=True)
    Produkt_ID = db.Column(db.Integer, db.ForeignKey('produkte.ID'), primary_key=True)
    Anzahl = db.Column(db.Integer)

    einkauf = relationship("Einkauf")
    produkte = relationship("Produkte")
