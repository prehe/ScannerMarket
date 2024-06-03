from flask_wtf import FlaskForm, form
from wtforms.fields import BooleanField, RadioField, SelectField, StringField, DecimalField,PasswordField, EmailField, DateField 
from wtforms.fields.simple import SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, URL,Email, EqualTo, Optional



class addProductForm(FlaskForm):
    name = StringField('Produktname', validators=[DataRequired(), Length(min=2, max=150)])
    manufacturer = StringField('Hersteller', validators=[DataRequired(), Length(min=2, max=150)])
    price = DecimalField('Preis', validators=[DataRequired(), NumberRange(min=0,max=100)]) #Preis muss zwischen 0 und 100€ sein
    weight = DecimalField('Gewicht, Volumen, Anzahl',validators=[DataRequired(), NumberRange(min=0.0)]) 
    unit = StringField('Einheit des Gewichts(kg, g), Volumen(l, ml), Anzahl(pcs)', validators=[DataRequired(), Length(min=1, max=3)])
    ean = StringField('EAN_Barcode', validators=[DataRequired(),Length(min=6, max=15)]) #EAN Barcodes zwischen 8 und 13 Stellen, da unser Supermarkt auch andere Codes nutzt etwas mehr Spielraum
    category_ID = SelectField('Kategorie', choices=[('', 'Bitte wählen'),('1', 'Backwaren'),('2', 'Konserven & Konfitüren'), ('3', 'Sonstiges'), ('4','Getränke'),('5', 'Fisch & Meeresfrüchte'), ('6','Tiefkühlwaren'),('7', 'Obst & Gemüse'), ('8', 'Gewürze & Saucen'), ('9', 'Fleischprodukte'), ('10', 'Milchprodukte'),('11', 'Pasta, Reis & Nüsse'), ('12', 'Süßwaren')], validators=[DataRequired()])
    img_url = StringField('Bild-URL', validators=[ URL(message='Bitte eine gültige URL zum Bild eingeben')])
    submit = SubmitField('Produkt hinzufügen', render_kw={"class": "btn-secondary btn-right"})

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Anmelden')


class RegistrationForm(FlaskForm):
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    geburtsdatum = DateField('Geburtsdatum', validators=[DataRequired()], format='%Y-%m-%d')
    email = EmailField('Email', validators=[DataRequired(), Email()])
    passwort = PasswordField('Passwort', validators=[DataRequired()])
    kundenkarte = BooleanField('Kundenkarte beantragen')
    newsletter = BooleanField('Newsletter aktivieren')
    agb = BooleanField('Zustimmung der ScannerMarket AGBs', validators=[DataRequired()])

class EditProfile(FlaskForm):
    Vorname = StringField('Vorname', validators=[DataRequired()])
    Nachname = StringField('Nachname', validators=[DataRequired()])
    Geburtsdatum = DateField('Geburtsdatum', validators=[DataRequired()], format='%Y-%m-%d')
    Email = EmailField('Email', validators=[DataRequired(), Email()])
    Passwort = PasswordField('Passwort')
    Passwort_new = PasswordField('neues Passwort', validators=[Optional(),Length(min=4),EqualTo('Passwort_conf', message='Passwörter müssen übereinstimmen')])
    Passwort_conf = PasswordField('neues Passwort bestätigen', validators=[Optional(),Length(min=4)])
    Kundenkarte = BooleanField('Kundenkarte beantragen')
    Newsletter = BooleanField('Newsletter aktivieren')
    submit = SubmitField('Änderungen übernehmen')

