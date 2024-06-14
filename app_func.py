from flask import Blueprint, Flask, jsonify, render_template, request, session, redirect, url_for, session, flash
import formulare as formulare
import pandas as pd
from model import db, Nutzer, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime, timedelta
from sqlalchemy.orm import joinedload
from faker import Faker
import random

func = Blueprint(__name__, import_name="app_func")


categoryNames={
    'category-bread' : "Backwaren",
    'category-can': "Konserven & Konfitüren",
    'category-coffee' : "Sonstiges",
    'category-drinks' : "Getränke",
    'category-fish' : "Fisch & Meeresfrüchte",
    'category-frozen' : "Tiefkühlwaren",
    'category-fruit' : "Obst & Gemüse",
    'category-herbs' : "Gewürze & Saucen",
    'category-meat' : "Fleischprodukte",
    'category-milk' : "Milchprodukte",
    'category-pasta' : "Pasta, Reis & Nüsse",
    'category-sweets' : "Süßwaren"
}



############################ TESTDATEN: Kunden ############################
# ChatGPT
# Erstelle einen Faker Generator
fake = Faker()
# ChatGPT
# Funktion um ein zufälliges Datum innerhalb eines Bereichs zu generieren
def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# ChatGPT
# Funktion um zufällige Kunden zu erstellen
def create_random_customers(num_customers):
    for _ in range(num_customers):
        vorname = fake.first_name()
        nachname = fake.last_name()
        geburtsdatum = random_date(date(1950, 1, 1), date(2005, 12, 31))
        email = f"{vorname[0].lower()}.{nachname.lower()}@example.com"
        passwort = fake.password()
        kundenkarte = random.choice([True, False])
        admin = False
        newsletter = random.choice([True, False])
        registriert_am = random_date(date(2020, 1, 1), date.today())

        # Annahme: `Nutzer.add_nutzer` ist die Methode zum Hinzufügen eines Nutzers in die Datenbank
        Nutzer.add_nutzer(
            vorname=vorname,
            nachname=nachname,
            geburtsdatum=geburtsdatum,
            email=email,
            passwort=passwort,
            kundenkarte=kundenkarte,
            admin=admin,
            newsletter=newsletter,
            registriert_am=registriert_am
        )
    


############################ TESTDATEN: EINKÄUFE ############################
# ChatGPT
# Funktion um ein zufälliges Datum und Zeit zu generieren
def random_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

# ChatGPT
# Funktion um zufällige Einkäufe zu erstellen
def create_random_purchases(num_purchases, min_user_id, max_user_id):
    for _ in range(num_purchases):
        nutzer_id = random.randint(min_user_id, max_user_id)
        zeitstempel_start = random_timestamp(datetime(2023, 1, 1), datetime.now())
        zeitstempel_ende = zeitstempel_start + timedelta(hours=random.randint(1, 5))  # Endzeit ist zufällig zwischen 1 und 5 Stunden nach Start

        Einkauf.add_einkauf(nutzer_id, zeitstempel_start, zeitstempel_ende)
        
############################ TESTDATEN: WARENKORB ############################
# ChatGPT
# Funktion um zufällige Anzahl zwischen 1 und 10 zu generieren
def random_quantity():
    return random.randint(1, 10)

# Funktion um zufälliges Datum und Zeit zu generieren
def random_datetime(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

# Funktion um zufällige Produkte für einen Einkauf zu erstellen und sie zum Warenkorb hinzuzufügen
def add_random_products_to_cart(einkauf_id, min_product_id, max_product_id):
    num_products = random.randint(5, 15)  # Zufällige Anzahl von Produkten pro Einkauf
    for _ in range(num_products):
        produkt_id = random.randint(min_product_id, max_product_id)
        anzahl = random_quantity()
        Warenkorb.add_to_cart(einkauf_id, produkt_id, anzahl)



# Hilfsfunktion zum schnellen Einfügen von Daten zur Datenbank
@func.route('/insertDB')
def insertDB():

    #########################
    # Basis-Insert DB:
    ########################
        
    # # ################    Produktkategorien
    # service.addProductCategories(categoryNames)


    # ################ Produkte aus xlsx
    # df = pd.read_excel("produkte.xlsx", usecols=["Hersteller", "Name", "Gewicht_Volumen", "EAN", "Preis", "Bild", "Kategorie_ID"])
    # # print(df)
    # for index, row in df.iterrows():
    #     bild = str(row['Bild'])
    #     print(bild)
    #     if pd.isna(bild) or bild is None or bild == 'nan' or bild == 'None' or bild == '':
    #         print("Bild is nan or None, skipping insertion.")
    #     else:
    #         produkt = Produkte(
    #             Hersteller=row['Hersteller'],
    #             Name=row['Name'],
    #             Gewicht_Volumen=row['Gewicht_Volumen'],
    #             EAN=row['EAN'],
    #             Preis=row['Preis'],
    #             Bild=bild,
    #             Kategorie_ID=row['Kategorie_ID']
    #         )
    #         db.session.add(produkt)
    # db.session.commit()

    


    # # ###############    Nutzer
    # Nutzer.add_nutzer(vorname="Peter", nachname="Muster", geburtsdatum=date(1990, 1, 1), email='hallo.test@email.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True) 
    # Nutzer.add_nutzer(vorname="Celli", nachname="Stern", geburtsdatum=date(1990, 1, 1), email='c.Stern@example.com', passwort='Stern', kundenkarte=True, admin=False, newsletter=True, registriert_am=date(2024,2,23))
    

    # Erstellen von 60 zufälligen Kunden
    # create_random_customers(60)





    ###################  Einkauf
    # Beispiel Nutzer IDs von 1 bis 67
    # min_user_id = 1
    # max_user_id = 67

    # # Erstellen von 300 zufälligen Einkäufen
    # create_random_purchases(300, min_user_id, max_user_id)

    ######################### WARENKÖRBE
    # Beispiel: Min und Max Werte für Einkauf und Produkt IDs
    min_einkauf_id = 19
    max_einkauf_id = 308
    min_produkt_id = 1
    max_produkt_id = 432

    # Füllen des Warenkorbs mit Testdaten
    for einkauf_id in range(min_einkauf_id, max_einkauf_id):
        add_random_products_to_cart(einkauf_id,  min_product_id=min_produkt_id, max_product_id=max_produkt_id)



    return redirect(url_for('app_customer.productcatalog'))


#  gibt die Produktinformatuionen von einer EAN zurück
@func.route('/getProductFromEan', methods=["GET"])
def getProductFromEan():
    search_ean = request.args.get('ean')
    try:
        produkt = db.session.query(Produkte).filter_by(EAN=search_ean).first()
        if produkt:
            print(produkt.to_dict())
            return jsonify(produkt.to_dict())
        else:
            flash('Produkt nicht gefunden', 'warning')
            return jsonify(error="Produkt nicht gefunden", redirect_url=url_for('app_customer.scanner'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('app_customer.scanner'))
        
 
# erhöht die Anzahl eines Produktes im Warenkorb
@func.route("/increase_cart_amount", methods=["POST"])
def increase_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    # print(einkauf_id, produkt_id, " aus der empfangenen URL: /increase_cart_amount")
    response = Warenkorb.increase_cart_amount(einkauf_id, produkt_id)
    price = Produkte.get_product(produkt_id).Preis
    if response == "limit reached":
        flash('maximale Anzahl pro Produkt erreicht (10)', 'warning')
    return jsonify({"success": response, 'price': price, 'redirect_url':url_for('app_customer.shoppinglist')})

# verringert die Anzahl eines Produktes im Warenkorb
@func.route("/decrease_cart_amount", methods=["POST"])
def decrease_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    # print(einkauf_id, produkt_id, " aus der empfangenen URL: /decrease_cart_amount")
    response = Warenkorb.decrease_cart_amount(einkauf_id, produkt_id)
    price = Produkte.get_product(produkt_id).Preis
    return jsonify({"success": response, 'price': price, 'redirect_url':url_for('app_customer.shoppinglist')})

# fügt ein Produkt zum Warenkorb hinzu
@func.route("/addProdToBasket", methods=["POST"])
def addProdToBasket():
    einkauf_id = session.get('shoppingID', None)
    product_id = request.form.get("productId")
    quantity = request.form.get("quantity")
    if not einkauf_id or not product_id or not quantity:
        flash("Fehlende Daten für den Warenkorb", "error")
        return jsonify(success=False, message="Fehlende Daten für den Warenkorb", redirect_url=url_for('app_customer.shoppinglist'))

    try:
        quantity = int(quantity)
    except ValueError:
        flash("Ungültige Mengenangabe", "error")
        return jsonify(success=False, message="Ungültige Mengenangabe", redirect_url=url_for('app_customer.shoppinglist'))

    basket_item = Warenkorb.query.filter_by(Einkauf_ID=einkauf_id, Produkt_ID=product_id).first()
    if basket_item:
        basket_item.Anzahl += quantity
        if basket_item.Anzahl > 10:
            basket_item.Anzahl = 10
            flash('maximale Anzahl pro Produkt erreicht (10)', 'warning')
    else:
        basket_item = Warenkorb(Einkauf_ID=einkauf_id, Produkt_ID=product_id, Anzahl=quantity)
        db.session.add(basket_item)
    
    db.session.commit()
    flash('Produkt erfolgreich zum Warenkorb hinzugefügt', 'success')
    return jsonify(success=True, redirect_url=url_for('app_customer.shoppinglist'))

# entfernt ein Produkt aus dem Warenkorb
@func.route("/deleteItemFromList", methods=["POST"])
def deleteItemFromList():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    response = Warenkorb.remove_from_cart(einkauf_id=einkauf_id, produkt_id=produkt_id)
    return jsonify(value=response, redirect_url=url_for('app_customer.shoppinglist'))

# beendet den Einkauf
@func.route("/purchase", methods=["POST"])
def purchase():
    response = Einkauf.add_endTimestamp(session.get('shoppingID', None), getTotalBasketPrice(session.get('shoppingID', None)))
    return jsonify({"success": response, 'redirect_url': url_for('app_customer.shoppingresult')})

# generiert einen QR-Code für die Bezahlung mit den Daten des Einkaufs
@func.route("/generateQR", methods=["GET"])
def generateQR():
    einkauf_id = session.get('shoppingID', None)
    preis = getTotalBasketPrice(einkauf_id)
    payment_URL = f"Einkauf_ID={einkauf_id}&Preis={preis}"
    session['shoppingID'] = None
    return payment_URL

# HILFSFUNKTION - gibt den Gesamtpreis des Warenkorbs zurück
def getTotalBasketPrice(einkauf_id):
    items = db.session.query(Warenkorb).\
    outerjoin(Warenkorb.einkauf).\
    join(Warenkorb.produkt).\
    filter(Warenkorb.Einkauf_ID == einkauf_id).\
    options(joinedload(Warenkorb.produkt)).all()

    total_price = round(sum(item.Anzahl * item.produkt.Preis for item in items), 2)
    return total_price