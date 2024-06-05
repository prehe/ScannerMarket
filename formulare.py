from flask_wtf import FlaskForm
from wtforms.fields import BooleanField,  SelectField, StringField, DecimalField,PasswordField, EmailField, DateField 
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, URL,Email, Optional


# Formular definieren, zum hinzufügen von neuen Produkten
class addProductForm(FlaskForm):
    name = StringField('Produktname', validators=[DataRequired(), Length(min=2, max=150)]) # Zeichenbegrenzung
    manufacturer = StringField('Hersteller', validators=[DataRequired(), Length(min=2, max=150)]) # Zeichenbegrenzung
    price = DecimalField('Preis', validators=[DataRequired(), NumberRange(min=0,max=100)]) # Preis muss zwischen 0 und 100€ sein
    weight = DecimalField('Gewicht, Volumen, Anzahl',validators=[DataRequired(), NumberRange(min=0.0)]) # Gewicht muss vorliegen 
    unit = StringField('Einheit des Gewichts(kg, g), Volumen(l, ml), Anzahl(pcs)', validators=[DataRequired(), Length(min=1, max=3)])
    ean = StringField('EAN_Barcode', validators=[DataRequired(),Length(min=6, max=15)]) # EAN Barcodes zwischen 8 und 13 Stellen, da unser Supermarkt auch andere Codes nutzt etwas mehr Spielraum
    category_ID = SelectField('Kategorie', choices=[('', 'Bitte wählen'),('1', 'Backwaren'),('2', 'Konserven & Konfitüren'), ('3', 'Sonstiges'), ('4','Getränke'),('5', 'Fisch & Meeresfrüchte'), ('6','Tiefkühlwaren'),('7', 'Obst & Gemüse'), ('8', 'Gewürze & Saucen'), ('9', 'Fleischprodukte'), ('10', 'Milchprodukte'),('11', 'Pasta, Reis & Nüsse'), ('12', 'Süßwaren')], validators=[DataRequired()])
    img_url = StringField('Bild-URL', validators=[ URL(message='Bitte eine gültige URL zum Bild eingeben')]) # Eingabe muss URL-Format einhalten
    submit = SubmitField('Produkt hinzufügen', render_kw={"class": "btn-secondary btn-right"})

# Login-Formular definieren
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # Email-Format muss eigenhalten werden
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Anmelden')

# Registrierungsformular definieren
class RegistrationForm(FlaskForm):
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    geburtsdatum = DateField('Geburtsdatum', validators=[DataRequired()], format='%Y-%m-%d')  # Datums-Format muss eigenhalten werden
    email = EmailField('Email', validators=[DataRequired(), Email()])
    passwort = PasswordField('Passwort', validators=[DataRequired(),Length(min=4)]) # Passwort muss mindestens 4 Zeichen haben
    passwort_new = PasswordField('Passwort bestätigen', validators=[Length(min=4)]) # Passwort muss mindestens 4 Zeichen haben
    kundenkarte = BooleanField('Kundenkarte beantragen')
    newsletter = BooleanField('Newsletter aktivieren')
    agb = BooleanField('Zustimmung der ScannerMarket AGBs', validators=[DataRequired()])

# Profilbearbeitungsformular definieren
class EditProfile(FlaskForm):
    Vorname = StringField('Vorname', validators=[DataRequired()])
    Nachname = StringField('Nachname', validators=[DataRequired()])
    Geburtsdatum = DateField('Geburtsdatum', validators=[DataRequired()], format='%Y-%m-%d')  # Datums-Format muss eigenhalten werden
    Email = EmailField('Email', validators=[DataRequired(), Email()])  # Email-Format muss eigenhalten werden
    Passwort = PasswordField('Passwort')
    Passwort_new = PasswordField('neues Passwort', validators=[Optional(),Length(min=4)]) # Feld ist optional --> wenn Inhalt: Passwort muss mindestens 4 Zeichen haben
    Passwort_conf = PasswordField('neues Passwort bestätigen', validators=[Optional(),Length(min=4)]) # Feld ist optional --> wenn Inhalt: Passwort muss mindestens 4 Zeichen haben
    Kundenkarte = BooleanField('Kundenkarte beantragen')
    Newsletter = BooleanField('Newsletter aktivieren')
    submit = SubmitField('Änderungen übernehmen')

