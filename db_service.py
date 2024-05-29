from datetime import date
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import pandas as pd
import requests
import time
import math

def addNewCustomer (vorname, nachname, geb_datum, email, passwort, kundenkarte, admin, newsletter):
    #einen neuen Kunden in die Datenbank einfügen
    customer = Nutzer(Vorname=vorname, Nachname=nachname, Geburtsdatum=geb_datum, Email=email, Passwort=passwort, Kundenkarte=kundenkarte, Admin=admin, Newsletter=newsletter, Registriert_am = date.today())
    db.session.add(customer)
    db.session.commit()

def addProductCategories (categoryNames):
    #Kategorien in die Datenbank einfügen
    for name in categoryNames.values():
        category = Produktkategorien(Kategorie = name)
        db.session.add(category)
    db.session.commit()

def addNewProduct(hersteller, produktname, gewicht_volumen, ean, preis, bild, kategorie):
     # Produkt in die Datenbank einfügen
        new_product = Produkte(
            Hersteller = hersteller,
            Name = produktname,
            Gewicht_Volumen = gewicht_volumen,
            EAN = ean,
            Preis = preis,
            Bild = bild,
            Kategorie_ID = kategorie
        )
        db.session.add(new_product)
        db.session.commit()
        db.session.close()
        print("erfolgreich hinzugefügt")

#Daten eines Produktes über den barcode aus der Datenbank abfragen
def get_and_save_product_data(barcode, price, categoryId):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        product_data = response.json()["product"]
        
        # Produktinformationen aus der API extrahieren
        ean = product_data['id']
        hersteller = product_data['brands']
        produktname = product_data['product_name']
        gewicht_volumen = product_data.get('quantity', '')  # 'quantity' könnte fehlen, daher verwenden wir 'get'
        kategorie = categoryId
        preis = price
        bild = product_data.get('image_front_small_url', '')

        addNewProduct(hersteller, produktname, gewicht_volumen, ean, preis, bild, kategorie)
              
        print("Produkt erfolgreich hinzugefügt!")
    else:
        print(f"Fehler beim Abrufen der Produktinformationen. Statuscode: {response.status_code}")

#barcodes einer Produktkategorie aus einer Excel-Liste auslesen
def getDataFromExcel(category):
    excel = "static\product_barcodes.xlsx"
    file = pd.read_excel(excel)
    if category in file.columns:
        barcodesOfCat = file[category].dropna().astype(str).str.replace('\.0', '', regex=True).tolist() #chatgpt
        pricesOfCat = file['Preis_'+category].tolist()
        # print(barcodesOfCat)
        return barcodesOfCat, pricesOfCat
    else:
        print(f"Spalte: '{category}' nicht gefunden")
        return

 #Produkte aus Excel-Liste zur Datenbank hinzufügen
def addAllProductsFromExcel (categoryNames):
    id = 1
    for name in categoryNames.values():
        output = getDataFromExcel(name)
        eans = [value for value in output[0] if not isinstance(value, float) or not math.isnan(value)]
        prices = [value for value in output[1] if not isinstance(value, float) or not math.isnan(value)]
        modified_output = (eans, prices)
        print(modified_output)

        for barcode, price in zip(modified_output[0], modified_output[1]):
            try:
                get_and_save_product_data(str(barcode), price, categoryId=id)
                time.sleep(1)  # Timeout wegen API-Zugriff
            except:
                print("Fehler bei: ", barcode, price)

        id = id+1
