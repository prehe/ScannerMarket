# app.py
from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date
from sqlalchemy.orm import joinedload

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Aktiviere CORS für alle Routen

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
    return render_template('sm_admin_analysis.html')

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
    prodsOfCategory = db.session.query(Produkte).join(Produktkategorien).filter(Produktkategorien.kategorie == category)
    for prod in prodsOfCategory:
        newProd = {'name': prod.produkt_name, 'img': prod.bild, 'weight' : prod.gewicht_volumen, 'price': prod.preis, 'manufacturer' : prod.hersteller}
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
        filter(Warenkorb.einkauf_ID == shopping_id).\
        options(joinedload(Warenkorb.produkte))  # Optional: Lädt die Produktdaten vor, um N+1 Abfragen zu vermeiden

    for prod in prodsOfCategory:
        newProd = {'name': prod.produkte.produkt_name, 'amount': prod.anzahl}
        products.append(newProd)
    return products

# ####################################################################################################################################################
#dürfen nur einsehbar sein, wenn eingelogter Nutzer ein Administrator ist

@app.route('/nutzer')
def show_nutzer():
    #Kunden hinzufügen
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='max.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True) 
    

    nutzer_entries = db.session.query(Nutzer).all()
    # print(nutzer_entries[0].ID)
    column_names = ["ID", "vorname", "nachname", "geb_datum", "email", "passwort", "kundenkarte", "admin", "newsletter"]
    return render_template('db_table_view.html', entries=nutzer_entries, column_names=column_names, title = "registrierte Kunden")

@app.route('/produktkategorien')
def show_produktkategorien():
    #Produktkategorien zur Datenbank einmalig hinzufügen
    #service.addProductCategories(categoryNames)

    produktkategorien_entries = db.session.query(Produktkategorien).all()
    column_names = ["ID", "kategorie"]
    return render_template('db_table_view.html',entries=produktkategorien_entries, column_names= column_names, title = "Produktkategorien")

@app.route('/produkte')
def show_produkte():
    #Alle Produkte aus der Excel-Tabelle in die Datenbank einfügen
    #service.addAllProductsFromExcel(categoryNames)  
    produkte_entries = db.session.query(Produkte).all()
    column_names = ["ID", "hersteller", "produkt_name", "gewicht_volumen", "ean", "preis","bild", "produktkategorien_ID"]
    return render_template('db_table_view.html', entries=produkte_entries, column_names= column_names, title = "Produkte")


####ToDo: auf Tabellenanzeige Template anpassen
@app.route('/einkauf')
def show_einkauf():
    einkauf_entries = db.session.query(Einkauf).all()
    return render_template('einkauf.html', einkauf_entries=einkauf_entries)

@app.route('/warenkorb')
def show_warenkorb():
    warenkorb_entries = db.session.query(Warenkorb).all()
    return render_template('warenkorb.html', warenkorb_entries=warenkorb_entries)

@app.route('/bezahlmöglichkeiten')
def show_bezahlmöglichkeiten():
    bezahlmoeglichkeiten_entries = db.session.query(Bezahlmöglichkeiten).all()
    return render_template('bezahlmöglichkeiten.html', bezahlmoeglichkeiten_entries=bezahlmoeglichkeiten_entries)

@app.route('/bezahlung')
def show_bezahlung():
    bezahlung_entries = db.session.query(Bezahlung).all()
    return render_template('bezahlung.html', bezahlungen_entries =bezahlung_entries)



@app.route('/produktkategorien')
def show_produktkategorien():
    #Produktkategorien zur Datenbank einmalig hinzufügen
    #service.addProductCategories(categoryNames)

    produktkategorien_entries = db.session.query(Produktkategorien).all()
    print(produktkategorien_entries)
    return render_template('produktkategorien.html', produktkategorien_entries=produktkategorien_entries)


@app.route('/produkte')
def show_produkte():
    #Alle Produkte aus der Excel-Tabelle in die Datenbank einfügen
    #service.addAllProductsFromExcel(categoryNames)  
    produkte_entries = db.session.query(Produkte).all()
    return render_template('produkte.html', produkte_entries=produkte_entries)

@app.route('/einkauf')
def show_einkauf():
    einkauf_entries = db.session.query(Einkauf).all()
    return render_template('einkauf.html', einkauf_entries=einkauf_entries)

@app.route('/warenkorb')
def show_warenkorb():
    warenkorb_entries = db.session.query(Warenkorb).all()
    return render_template('warenkorb.html', warenkorb_entries=warenkorb_entries)


##################### besondere URLs/Funktionen:

@app.route('/insertDB')
def insertDB():
    # service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='max.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True) 
    # service.addNewCustomer(vorname="Paulchen", nachname="Kleiner", geb_datum=date(1990, 1, 1), email='p.kleiner@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True)
    # paymethod = Bezahlmöglichkeiten(methode="Paypal")
    # db.session.add(paymethod)
    # db.session.commit()
    # paymethod = Bezahlmöglichkeiten(methode="Kreditkarte")
    # db.session.add(paymethod)
    # db.session.commit()

    # pay = Bezahlung(nutzer_ID = 1, bezahlmöglichkeiten_ID = 1, konto_email = "p.kleiner@example.com")
    # db.session.add(pay)
    # db.session.commit()
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
