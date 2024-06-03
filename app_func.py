from flask import Blueprint, Flask, jsonify, render_template, request, session, redirect, url_for, session, flash
import formulare as formulare
import pandas as pd
import requests
from model import db, Nutzer, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload

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
    #     produkt = Produkte(
    #         Hersteller=row['Hersteller'],
    #         Name=row['Name'],
    #         Gewicht_Volumen=row['Gewicht_Volumen'],
    #         EAN=row['EAN'],
    #         Preis=row['Preis'],
    #         Bild=row['Bild'],
    #         Kategorie_ID=row['Kategorie_ID']
    #     )
    #     db.session.add(produkt)
    # db.session.commit()


    # ###############    Nutzer
    # Nutzer.add_nutzer(vorname="Peter", nachname="Muster", geburtsdatum=date(1990, 1, 1), email='hallo.test@email.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True) 
    # Nutzer.add_nutzer(vorname="Celli", nachname="Stern", geburtsdatum=date(1990, 1, 1), email='c.Stern@example.com', passwort='Stern', kundenkarte=True, admin=True, newsletter=True)
    
    # # #################  Einkauf
    # something = Einkauf(Nutzer_ID = 2)
    # db.session.add(something)
    # db.session.commit()

    # products_to_add = [(44,3), (46,3), (100,3),(33,3),(150,3),(200,3), (250,3), (300,3),(290,3),(400,3), (234,3), (287,3), (76,3)]

    # # Loop through the list of products and add them to the shopping cart
    # for produkte_ID, quantity in products_to_add:
    #     new_item = Warenkorb(Einkauf_ID=2, Produkt_ID=produkte_ID, Anzahl=quantity)
    #     db.session.add(new_item)
    # db.session.commit()
    # Einkauf.resetTable()

    return redirect(url_for('app_customer.productcatalog'))
 
 
 
@func.route('/getProductFromEan', methods=["GET"])
def getProductFromEan():
    search_ean = request.args.get('ean')
    try:
        produkt = db.session.query(Produkte).filter_by(EAN=search_ean).first()
        if produkt:
            return jsonify(produkt.to_dict())
        else:
            return jsonify({'error': 'Produkt nicht gefunden'}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
        
 
 
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

@func.route("/decrease_cart_amount", methods=["POST"])
def decrease_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    # print(einkauf_id, produkt_id, " aus der empfangenen URL: /decrease_cart_amount")
    response = Warenkorb.decrease_cart_amount(einkauf_id, produkt_id)
    price = Produkte.get_product(produkt_id).Preis
    return jsonify({"success": response, 'price': price, 'redirect_url':url_for('app_customer.shoppinglist')})

@func.route("/purchase", methods=["POST"])
def purchase():
    response = Einkauf.add_endTimestamp(session.get('shoppingID', None))
    session['shoppingID'] = None
    return jsonify({"success": response, 'redirect_url': url_for('app_customer.productcatalog')})


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


@func.route("/deleteItemFromList", methods=["POST"])
def deleteItemFromList():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    response = Warenkorb.remove_from_cart(einkauf_id=einkauf_id, produkt_id=produkt_id)
    return jsonify(value=response, redirect_url=url_for('app_customer.shoppinglist'))

@func.route("/generateQR", methods=["GET"])
def generateQR():
    einkauf_id = session.get('shoppingID', None)
    preis = getTotalBasketPrice(einkauf_id)
    payment_URL = f"Einkauf_ID={einkauf_id}&Preis={preis}"
    return payment_URL

def getTotalBasketPrice(einkauf_id):
    items = db.session.query(Warenkorb).\
    outerjoin(Warenkorb.einkauf).\
    join(Warenkorb.produkt).\
    filter(Warenkorb.Einkauf_ID == einkauf_id).\
    options(joinedload(Warenkorb.produkt)).all()

    total_price = round(sum(item.Anzahl * item.produkt.Preis for item in items), 2)
    return total_price