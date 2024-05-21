from flask_wtf import FlaskForm, form
from wtforms.fields import BooleanField, RadioField, SelectField, StringField, DecimalField
from wtforms.fields.simple import SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, URL

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