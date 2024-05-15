# app.py
from flask import Flask, render_template, request
#from flask_cors import CORS
import pandas as pd
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload
 
# Initialize the Flask application
app = Flask(__name__)
#CORS(app)  # Aktiviere CORS für alle Routen
 
# Verbindung zur Datenbank herstellen
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scannerMarket.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
 
 
# Define the root route
@app.route('/')
def index():
    # Render the default template
    return render_template('sm_cust_main.html')
 
# Define the route for the default page
@app.route('/main')
def defaultP():
    return render_template('sm_cust_main.html')
 
@app.route('/registration')
def registrationP():
    return render_template('sm_registration.html')
 
@app.route('/login')
def loginP():
    return render_template('sm_login.html')
 
@app.route('/scanner')
def scannerP():
    return render_template('sm_scanner.html')
 
@app.route('/shoppinglist')
def prodBasketP():
    return render_template('sm_shopping_list.html', product_list = getProdsFromShoppingList(1))
 
@app.route('/productcatalog')
def productcatalog():
    return render_template('sm_cust_main.html')
 
@app.route('/admin')
def adminMain():
    return render_template('sm_admin_main.html')
 
@app.route('/admin/newProduct')
def newProduct():
    return render_template('sm_admin_newProduct.html')
 
@app.route('/admin/analysis')
def analysis():
    return render_template('sm_admin_analysis.html', analyse_page= "/Produktkategorien")
 
#globale Variable
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
 
 
@app.route("/category/<category>")
def categoryPage(category):
    bannerImages={
        'category-bread' : "../static/images/category-bread.jpg",
        'category-can': "../static/images/category-can.jpg",
        'category-coffee' : "../static/images/category-coffee.jpg",
        'category-drinks' : "../static/images/category-drinks.jpg",
        'category-fish' : "../static/images/category-fish.jpg",
        'category-frozen' : "../static/images/category-frozen.jpg",
        'category-fruit' : "../static/images/category-fruit.jpg",
        'category-herbs' : "../static/images/category-herbs.jpg",
        'category-meat' : "../static/images/category-meat.jpg",
        'category-milk' : "../static/images/category-milk.jpg",
        'category-pasta' : "../static/images/category-pasta.jpg",
        'category-sweets' : "../static/images/category-sweets.jpg"
    }
    bannerImg = bannerImages[category]
    categoryName = categoryNames[category]
    products = getProdsFromCategory(categoryName)
    #products = [{'name': 'fertig', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'12.0', 'manufacturer':'wert' },{'name': 'roggen', 'img':'../static/images/category-sweets.jpg', 'weight': '3.0', 'price':'4.0', 'manufacturer':'hello' },{'name': 'test', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'2.0', 'manufacturer':'tt' },{'name': 'brot', 'img':'../static/images/category-sweets.jpg', 'weight': '0.5', 'price':'6.0', 'manufacturer':'gmnt' }, {'name': 'cc', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'2.0', 'manufacturer':'tt' },{'name': 'test', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'2.0', 'manufacturer':'tt' }]
    return render_template('sm_category_page.html', category= categoryName, products=products, banner= bannerImg)
 
 
def getProdsFromCategory(category):
    products = []
    prodsOfCategory = db.session.query(Produkte).join(Produktkategorien).filter(Produktkategorien.Kategorie == category)
    for prod in prodsOfCategory:
        newProd = {'name': prod.Name, 'img': prod.Bild, 'weight' : prod.Gewicht_Volumen, 'price': prod.Preis, 'manufacturer' : prod.Hersteller}
        products.append(newProd)
    return products
 
@app.route("/impressum")
def impressum ():
    return render_template('sm_impressum.html')
 
def getProdsFromShoppingList(shopping_id):
    products = []
    prodsOfCategory = db.session.query(Warenkorb).\
        outerjoin(Warenkorb.einkauf).\
        join(Warenkorb.produkte).\
        filter(Warenkorb.Einkauf_ID == shopping_id).\
        options(joinedload(Warenkorb.produkte))  # Optional: Lädt die Produktdaten vor, um N+1 Abfragen zu vermeiden
 
    for prod in prodsOfCategory:
        newProd = {'shoppingCard_id': prod.Einkauf_ID,'prod_id': prod.Produkt_ID,'name': prod.produkte.Name, 'amount': prod.Anzahl}
        products.append(newProd)
    return products
 
# ####################################################################################################################################################
#dürfen nur einsehbar sein, wenn eingelogter Nutzer ein Administrator ist
 
@app.route('/Kunden')
def show_nutzer():
    #Kunden hinzufügen
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='ma.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am= date(2024, 5, 14))
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='peter.muster@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am =date(2024,5,15))
   
    nutzer_entries = db.session.query(Nutzer).all()
    # print(nutzer_entries[0].ID)
    column_names = ["ID", "Vorname", "Nachname", "Geburtsdatum", "Email", "Passwort", "Kundenkarte", "Admin", "Newsletter", " Registriert_am"]
    return render_template('db_table_view.html', entries=nutzer_entries, column_names=column_names, title = "registrierte Kunden")
 
@app.route('/Produktkategorien')
def show_produktkategorie():
    #Produktkategorien zur Datenbank einmalig hinzufügen
    #service.addProductCategories(categoryNames)
 
    produktkategorien_entries = db.session.query(Produktkategorien).all()
    column_names = ["ID", "Kategorie"]
    return render_template('db_table_view.html',entries=produktkategorien_entries, column_names= column_names, title = "Produktkategorien")
 
@app.route('/Produkte')
def show_produkte():
    #Alle Produkte aus der Excel-Tabelle in die Datenbank einfügen
    # service.addAllProductsFromExcel(categoryNames)  
    produkte_entries = db.session.query(Produkte).all()
    column_names = ["ID", "Hersteller", "Name", "Gewicht_Volumen", "EAN", "Preis","Bild", "Kategorie_ID"]
    return render_template('db_table_view.html', entries=produkte_entries, column_names= column_names, title = "Produkte")
 
 
####ToDo: auf Tabellenanzeige Template anpassen
@app.route('/Einkauf')
def show_einkauf():
    einkauf_entries = db.session.query(Einkauf).all()
    column_names =["ID", "Nutzer_ID",  "Zeitstempel_start","Zeitstempel_ende" ]
    return render_template('db_table_view.html', entries=einkauf_entries, column_names=column_names, title = "Einkauf")
 
@app.route('/Warenkorb')
def show_warenkorb():
    warenkorb_entries = db.session.query(Warenkorb).all()
    column_names = ["Einkauf_ID", "Produkt_ID", "Anzahl"]
    return render_template('db_table_view.html', entries=warenkorb_entries, column_names=column_names, title = "Warenkorb")
 
@app.route('/Bezahlmöglichkeiten')
def show_bezahlmöglichkeiten():
    bezahlmoeglichkeiten_entries = db.session.query(Bezahlmöglichkeiten).all()
    column_names = ["ID", "Methode"]
    return render_template('db_table_view.html', entries=bezahlmoeglichkeiten_entries, column_names=column_names, title="Bezahlmöglichkeiten")
 
@app.route('/Bezahlung')
def show_bezahlung():
    bezahlung_entries = db.session.query(Bezahlung).all()
    column_names = ["Nutzer_ID", "Bezahlmöglichkeiten_ID", "PP_Email", "Karten_Nr", "Karte_Gültingkeitsdatum", "Karte_Prüfnummer" ]
    return render_template('db_table_view.html', entries =bezahlung_entries, column_names=column_names, title = "Bezahlung")
 
@app.route('/Umsatz')
def show_umsatz():
    return render_template('umsatz.html',title = "Umsatz")
 
@app.route('/Neukunden')
def show_neukunden():
    return render_template('neukunden.html',title = "Neukunden")
 
##################### besondere URLs/Funktionen:
 
@app.route('/insertDB')
def insertDB():
    # service.addNewCustomer(Vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='max.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am =datetime(2024,5,15))
    # service.addNewCustomer(vorname="Paulchen", nachname="Kleiner", geb_datum=date(1990, 1, 1), email='p.kleiner@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True)
    # paymethod = Bezahlmöglichkeiten(methode="Paypal")
    # db.session.add(paymethod)
    # db.session.commit()
    # paymethod = Bezahlmöglichkeiten(Methode="Kreditkarte")
    # db.session.add(paymethod)
    # db.session.commit()
 
    # pay = Bezahlung(nutzer_ID = 1, bezahlmöglichkeiten_ID = 1, konto_email = "p.kleiner@example.com")
    # db.session.add(pay)
    # db.session.commit()

    something = Einkauf(Nutzer_ID = 2)
    db.session.add(something)
    db.session.commit()

    something = Warenkorb(Einkauf_ID=1, Produkt_ID = 3, Anzahl = 5)
    db.session.add(something)
    something2 = Warenkorb(Einkauf_ID=1, Produkt_ID = 2, Anzahl = 2)
    db.session.add(something2)
    

    products_to_add = [
    (7, 1),  # Tuple of (produkte_ID, quantity)
    (8, 2),
    (9, 1),
    (10, 3),
    (11, 1),
    (12, 2),
    (13, 1),
    (14, 1),
    (15, 2),
    (16, 1)]

    # Loop through the list of products and add them to the shopping cart
    for produkte_ID, quantity in products_to_add:
        new_item = Warenkorb(Einkauf_ID=1, Produkt_ID=produkte_ID, Anzahl=quantity)
        db.session.add(new_item)
    db.session.commit()

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
 
    produkte_entries = db.session.query(Produkte).all()
    return render_template('produkte.html', produkte_entries=produkte_entries)
 
 
 
@app.route('/getProductFromEan', methods=["GET", "POST"])
def getProductFromEan():
    search_ean = request.args.get('ean')  # Use request.args for query parameters
    print(search_ean)
    produkte_entries = db.session.query(Produkte).filter_by(ean=search_ean).all()
    print(produkte_entries)
    return produkte_entries
 
 
@app.route('/startOrEndShopping', methods=["GET", "POST"])
def startShopping():
    # peudo code:
    # if last tmst_end = none & nutzer_id = nutzer_id:
        # add tmst_end
    # else:
        # set new shopping(nutzer_id, tmst_start)
        # return shopping_id
        return None
 
 
 
 
# ####################################################################################################################################################
 
# Run the Flask application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
   
# Liveserver nicht mehr möglich mit den child templates
# app.py ausführen mit STRG+C stoppen und mit dem folgenden Befehl dauerhaft laufen lassen
# python -m flask --app app.py run --debug
# dann muss nur die Seite aktualiesiert werden und nicht immer app.py neu gestartet werden