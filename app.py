# app.py
from flask import Flask, render_template, request
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb

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

@app.route("/category/<category>")
#@app.route('/templates/sm_category_page/<category>')
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
    categoryNames={
        'category-bread' : "Backwaren",
        'category-can': "Konserven & Konfitüre",
        'category-coffee' : "Sonstiges",
        'category-drinks' : "Getränke",
        'category-fish' : "Fisch & Meeresfrüchte",
        'category-frozen' : "Tiefkühlwaren",
        'category-fruit' : "Obst & Gemüse",
        'category-herbs' : "Gewürze & Saucen",
        'category-meat' : "Fleisch",
        'category-milk' : "Milchprodukte",
        'category-pasta' : "Pasta, Reis & Nüsse", 
        'category-sweets' : "Süßwaren"
    }
    bannerImg = bannerImages[category]
    category = categoryNames[category]
    products = [{'name': 'fertig', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'12.0', 'manufacturer':'wert' },{'name': 'roggen', 'img':'../static/images/category-sweets.jpg', 'weight': '3.0', 'price':'4.0', 'manufacturer':'hello' },{'name': 'test', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'2.0', 'manufacturer':'tt' },{'name': 'brot', 'img':'../static/images/category-sweets.jpg', 'weight': '0.5', 'price':'6.0', 'manufacturer':'gmnt' }, {'name': 'cc', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'2.0', 'manufacturer':'tt' },{'name': 'test', 'img':'../static/images/category-sweets.jpg', 'weight': '3.5', 'price':'2.0', 'manufacturer':'tt' }]
    return render_template('sm_category_page.html', category= category, products=products, banner= bannerImg)

# from model import db, Nutzer
# from datetime import date

@app.route('/nutzer')
def show_nutzer():
    # beispiel_nutzer = Nutzer(vorname='Max', nachname='Mustermann', geb_datum=date(1990, 1, 1), email='max.mustermann@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True)
    # db.session.add(beispiel_nutzer)
    # db.session.commit()

    # nutzer_entries = Nutzer.query.all() 
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
    produktkategorien_entries = db.session.query(Produktkategorien).all()
    return render_template('produktkategorien.html', produktkategorien_entries=produktkategorien_entries)

@app.route('/produkte')
def show_produkte():
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



# Run the Flask application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
# Liveserver nicht mehr möglich mit den child templates
# app.py ausführen mit STRG+C stoppen und mit dem folgenden Befehl dauerhaft laufen lassen 
# python -m flask --app app.py run --debug
# dann muss nur die Seite aktualiesiert werden und nicht immer app.py neu gestartet werden
