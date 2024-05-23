from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, session, flash
import formulare as formulare
import pandas as pd
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload


func = Blueprint(__name__, import_name="app_func")


@func.route('/insertDB')
def insertDB():
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='hallo.test@email.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am =date(2024,5,15)) 
    #service.addNewCustomer(vorname="Celli", nachname="Stern", geb_datum=date(1990, 1, 1), email='c.Stern@example.com', passwort='Stern', kundenkarte=True, admin=True, newsletter=True, reg_am =date(2024,5,15))
    # paymethod = Bezahlmöglichkeiten(methode="Paypal")
    # db.session.add(paymethod)
    # db.session.commit()
    # paymethod = Bezahlmöglichkeiten(methode="Kreditkarte")
    # db.session.add(paymethod)
    # db.session.commit()

    # something = Einkauf(Nutzer_ID = 2)
    # db.session.add(something)
    # db.session.commit()

    # something = Warenkorb(Einkauf_ID=1, Produkt_ID = 3, Anzahl = 5)
    # db.session.add(something)
    # something2 = Warenkorb(Einkauf_ID=1, Produkt_ID = 2, Anzahl = 2)
    # db.session.add(something2)
    

    # products_to_add = [
    # (7, 1),  # Tuple of (produkte_ID, quantity)
    # (8, 2),
    # (9, 1),
    # (10, 3),
    # (11, 1),
    # (12, 2),
    # (13, 1),
    # (14, 1),
    # (15, 2),
    # (16, 1)]

    # # Loop through the list of products and add them to the shopping cart
    # for produkte_ID, quantity in products_to_add:
    #     new_item = Warenkorb(Einkauf_ID=1, Produkt_ID=produkte_ID, Anzahl=quantity)
    #     db.session.add(new_item)
    # db.session.commit()

    # service.addProductCategories(categoryNames)
    # service.addAllProductsFromExcel(categoryNames)
    # prod = Produkte(hersteller = 'ABC GmbH', produkt_name = "dummy3", produktkategorien_ID = 2)
    # db.session.add(prod)
    # db.session.commit()
 
    # something = Einkauf(nutzer_ID = 2)
    # db.session.add(something)
    # db.session.commit()
 
    # something = Warenkorb(einkauf_ID=1, produkte_ID = 3, anzahl = 5)
    # db.session.add(something)
    # # something2 = Warenkorb(einkauf_ID=1, produkte_ID = 2, anzahl = 2)
    # # db.session.add(something2)
    # db.session.commit()
 
    # service.addProductCategories(categoryNames)
    # service.addAllProductsFromExcel(categoryNames)

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
 
    #produkte_entries = db.session.query(Produkte).all()
    #return render_template('produkte.html', produkte_entries=produkte_entries)
    #produkte_entries = db.session.query(Produkte).all()
    return redirect(url_for('app_customer.productcatalog'))
 
 
 
@func.route('/getProductFromEan', methods=["POST"])
def getProductFromEan():
    search_ean = request.args.get('ean')  # Use request.args for query parameters
    print(search_ean)
    produkte_entries = db.session.query(Produkte).filter_by(ean=search_ean).all()
    print(produkte_entries)
    return produkte_entries
 
 
# @func.route('/startOrEndShopping', methods=["GET", "POST"])
# def startShopping():
#     # peudo code:
#     # if last tmst_end = none & nutzer_id = nutzer_id:
#         # add tmst_end
#     # else:
#         # set new shopping(nutzer_id, tmst_start)
#         # return shopping_id
#         return None


#############################################################################################################################################
# funktions-URLs:
@func.route("/increase_cart_amount", methods=["POST"])
def increase_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    print(einkauf_id, produkt_id, " aus der empfangenen URL: /increase_cart_amount")
    response = Warenkorb.increase_cart_amount(einkauf_id, produkt_id)
    return response

@func.route("/decrease_cart_amount", methods=["POST"])
def decrease_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    print(einkauf_id, produkt_id, " aus der empfangenen URL: /decrease_cart_amount")
    response = Warenkorb.decrease_cart_amount(einkauf_id, produkt_id)
    return response