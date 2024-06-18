from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

# Klasse, die die Nutzer-Tabelle repräsentiert
class Nutzer(db.Model):
    __tablename__ = 'nutzer'

    ID = db.Column(db.Integer, primary_key=True)
    Vorname = db.Column(db.String(200))
    Nachname = db.Column(db.String(200))
    Geburtsdatum = db.Column(db.Date)
    Email = db.Column(db.String(200), nullable=False, unique=True)
    Passwort = db.Column(db.String(50), nullable=False)
    Kundenkarte = db.Column(db.Boolean)
    Admin = db.Column(db.Boolean)
    Newsletter = db.Column(db.Boolean)
    Registriert_am = db.Column(db.Date)

    # Methode zum Hinzufügen eines neuen Nutzers
    @classmethod
    def add_nutzer(cls, vorname, nachname, geburtsdatum, email, passwort, kundenkarte=False, admin=False, newsletter=False, registriert_am=date.today()):
        new_nutzer = cls(Vorname=vorname, Nachname=nachname, Geburtsdatum=geburtsdatum, Email=email, Passwort=passwort, Kundenkarte=kundenkarte, Admin=admin, Newsletter=newsletter, Registriert_am=registriert_am)
        db.session.add(new_nutzer)
        db.session.commit()
        return new_nutzer

# Klasse, die die Produktkategorien-Tabelle repräsentiert
class Produktkategorien(db.Model):
    __tablename__ = 'produktkategorien'

    ID = db.Column(db.Integer, primary_key=True)
    Kategorie = db.Column(db.String(45))

# Klasse, die die Produkte-Tabelle repräsentiert
class Produkte(db.Model):
    __tablename__ = 'produkte'

    ID = db.Column(db.Integer, primary_key=True)
    Hersteller = db.Column(db.String(200))
    Name = db.Column(db.String(200))
    Gewicht_Volumen = db.Column(db.String(45))
    EAN = db.Column(db.BigInteger)
    Preis = db.Column(db.Float)
    Bild = db.Column(db.String(1500))  
    Kategorie_ID = db.Column(db.Integer, db.ForeignKey('produktkategorien.ID'))

    produktkategorien = relationship("Produktkategorien")

    # Methode, um Produktdetails als Dictionary zurückzugeben
    def to_dict(self):
        return {
            'ID': self.ID,
            'Hersteller': self.Hersteller,
            'Name': self.Name,
            'Gewicht_Volumen': self.Gewicht_Volumen,
            'EAN': self.EAN,
            'Preis': self.Preis,
            'Bild': self.Bild,
            'Kategorie_ID': self.Kategorie_ID,
        }

    # Methode, um ein Produkt anhand der Produkt-ID zu holen
    @classmethod
    def get_product(cls, product_id):
        product = Produkte.query.filter_by(ID=product_id).first()
        return product
    
    @classmethod
    def addNewProduct(cls, hersteller, produktname, gewicht_volumen, ean, preis, bild, kategorie):
        bild = str(bild)

        if bild == 'nan' or bild == 'None' or bild == '':
            print("Bild is nan or None or empty, skipping insertion.")
        else:
            new_product = cls(
                Hersteller=hersteller,
                Name=produktname,
                Gewicht_Volumen=gewicht_volumen,
                EAN=ean,
                Preis=preis,
                Bild=bild,
                Kategorie_ID=kategorie
            )
            db.session.add(new_product)
            db.session.commit()


# Klasse, die die Einkauf-Tabelle repräsentiert
class Einkauf(db.Model):
    __tablename__ = 'einkauf'

    ID = db.Column(db.Integer, primary_key=True)
    Nutzer_ID = db.Column(db.Integer, db.ForeignKey('nutzer.ID'))
    Zeitstempel_start = db.Column(db.DateTime)
    Zeitstempel_ende = db.Column(db.DateTime)
    Preis = db.Column(db.Float)
    Bezahlt = db.Column(db.Boolean)

    nutzer = relationship("Nutzer")

    # Methode zum Hinzufügen eines neuen Einkaufs
    @classmethod
    def add_einkauf(cls, nutzer_id, zeitstempel_start=None, zeitstempel_ende=None):
        if zeitstempel_start is None:
            zeitstempel_start = datetime.now()

        neuer_einkauf = cls(
            Nutzer_ID=nutzer_id,
            Zeitstempel_start=zeitstempel_start,
            Zeitstempel_ende=zeitstempel_ende
        )

        db.session.add(neuer_einkauf)
        db.session.commit()
        return neuer_einkauf.ID

    # Methode zum Hinzufügen eines Endzeitstempels und Preises
    @classmethod
    def add_endTimestamp(cls, einkauf_id, preis):
        einkauf = cls.query.filter_by(ID=einkauf_id).first()
        if einkauf:
            einkauf.Zeitstempel_ende = datetime.now()
            einkauf.Preis = preis
            db.session.commit()
            return True
        else:
            return False

    # Methode, um einen Einkauf als bezahlt zu markieren
    @classmethod
    def payment_done(cls, einkauf_id):
        einkauf = cls.query.filter_by(ID=einkauf_id).first()
        if einkauf:
            einkauf.Bezahlt = True
            db.session.commit()
            return True
        else:
            return False

    # Methode zum Zurücksetzen der Tabelle (löschen aller Einträge)
    @classmethod
    def resetTable(cls):
        cls.query.delete()
        db.session.commit()

# Klasse, die die Warenkorb-Tabelle repräsentiert
class Warenkorb(db.Model):
    __tablename__ = 'warenkorb'

    Einkauf_ID = db.Column(db.Integer, db.ForeignKey('einkauf.ID'), primary_key=True)
    Produkt_ID = db.Column(db.Integer, db.ForeignKey('produkte.ID'), primary_key=True, autoincrement=False, nullable=False)
    Anzahl = db.Column(db.Integer)

    einkauf = relationship("Einkauf")
    produkt = relationship("Produkte")



    # Methode zum Hinzufügen eines Produkts zum Warenkorb mit Überprüfung
    @classmethod
    def add_to_cart(cls, einkauf_id, produkt_id, anzahl):
        existing_entry = cls.query.filter_by(Einkauf_ID=einkauf_id, Produkt_ID=produkt_id).first()
        if existing_entry:
            # Eintrag existiert bereits, hier könnte man eine Aktualisierung vornehmen oder eine Exception werfen
            return existing_entry

        warenkorb = cls(Einkauf_ID=einkauf_id, Produkt_ID=produkt_id, Anzahl=anzahl)
        db.session.add(warenkorb)
        db.session.commit()
        return warenkorb


    # Methode zum Aktualisieren der Anzahl eines Produkts im Warenkorb
    @classmethod
    def update_quantity(cls, einkauf_id, produkt_id, neue_anzahl):
        ware = cls.query.filter_by(Einkauf_ID=einkauf_id, Produkt_ID=produkt_id).first()
        if ware:
            ware.Anzahl = neue_anzahl
            db.session.commit()

    # Methode zum Entfernen eines Produkts aus dem Warenkorb
    @classmethod
    def remove_from_cart(cls, einkauf_id, produkt_id):
        ware = cls.query.filter_by(Einkauf_ID=einkauf_id, Produkt_ID=produkt_id).first()
        if ware:
            db.session.delete(ware)
            db.session.commit()
            return "removed"
        else:
            return "item not found"

    # Methode zum Erhöhen der Anzahl eines Produkts im Warenkorb
    @classmethod
    def increase_cart_amount(cls, einkauf_id, produkt_id):
        ware = cls.query.filter_by(Einkauf_ID=einkauf_id, Produkt_ID=produkt_id).first()
        if ware:
            if ware.Anzahl < 10:
                ware.Anzahl = ware.Anzahl + 1
                db.session.commit()
                return "increased"
            else:
                return "limit reached"

    # Methode zum Verringern der Anzahl eines Produkts im Warenkorb
    @classmethod
    def decrease_cart_amount(cls, einkauf_id, produkt_id):
        ware = cls.query.filter_by(Einkauf_ID=einkauf_id, Produkt_ID=produkt_id).first()
        if ware is None:
            return "error"  # handle case where the item is not found
        if ware.Anzahl > 1:
            ware.Anzahl -= 1
            db.session.commit()
            return "decreased"
        else:
            return "no change"  # indicate that no change was made because the amount is already 1

    # Methode zum Abrufen des Inhalts des Warenkorbs für einen bestimmten Einkauf
    @classmethod
    def get_cart_contents(cls, einkauf_id):
        return cls.query.filter_by(Einkauf_ID=einkauf_id).all()

    # Methode zum Zurücksetzen der Tabelle (löschen aller Einträge)
    @classmethod
    def resetTable(cls):
        cls.query.delete()
        db.session.commit()
