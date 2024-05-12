# app.py
from flask import Flask, render_template
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date

# Initialize the Flask application
app = Flask(__name__)

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
@app.route('/templates/sm_cust_main.html')
def defaultP():
    return render_template('sm_cust_main.html')

@app.route('/templates/sm_registration.html')
def registrationP():
    return render_template('sm_registration.html')

@app.route('/templates/sm_login.html')
def loginP():
    return render_template('sm_login.html')

@app.route('/templates/sm_scanner.html')
def scannerP():
    return render_template('sm_scanner.html')

@app.route('/templates/sm_productbasket.html')
def prodBasketP():
    return render_template('sm_productbasket.html')

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

# ####################################################################################################################################################
#dürfen nur einsehbar sein, wenn eingelogter Nutzer ein Administrator ist

@app.route('/nutzer')
def show_nutzer():
    #Kunden hinzufügen
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='max.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True) 
    
    nutzer_entries = db.session.query(Nutzer).all()
    # print(nutzer_entries[0].ID)
    return render_template('nutzer.html', nutzer_entries=nutzer_entries)

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


def get_and_save_product_data(barcode, categoryId):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        product_data = response.json()["product"]
        
        # Produktinformationen aus der API extrahieren
        ean = product_data['id']
        hersteller = product_data['brands']
        produktname = product_data['product_name']
        gewicht_volumen = product_data.get('quantity', '')  # 'quantity' könnte fehlen, daher verwenden wir 'get'
        kategorie = categoryId
        preis = 0  # TODO: Preis aus dem Globus Online Produktkatalog abrufen
        bild = product_data.get('image_front_small_url', '')

        addNewProduct(hersteller, produktname, gewicht_volumen, ean, preis, bild, kategorie)
              
        print("Produkt erfolgreich hinzugefügt!")
    else:
        print(f"Fehler beim Abrufen der Produktinformationen. Statuscode: {response.status_code}")


def addNewProduct(hersteller, produktname, gewicht_volumen, ean, preis, bild, kategorie):
     # Produkt in die Datenbank einfügen
        new_product = Produkte(
            hersteller = hersteller,
            produkt_name = produktname,
            gewicht_volumen = gewicht_volumen,
            ean = ean,
            preis = preis,
            bild = bild,
            produktkategorien_ID = kategorie
        )
        db.session.add(new_product)
        db.session.commit()
        db.session.close()

def getBarcodesOfCategory(category):
    excel = "static\product_barcodes.xlsx"
    file = pd.read_excel(excel)
    if category in file.columns:
        barcodesOfCat = file[category].dropna().astype(str).str.replace('\.0', '', regex=True).tolist() #chatgpt
        # print(barcodesOfCat)
        return barcodesOfCat
    else:
        print(f"Spalte: '{category}' nicht gefunden")
        return


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

import db_service

@app.route('/DB')
def getData():
    produkte_entries = db_service.getProductFromEAN(4061458042918)
    print(produkte_entries)
    # return render_template('produkte.html', produkte_entries=produkte_entries)

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
