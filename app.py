# app.py
from flask import Flask, render_template, request, session, redirect, url_for, session, flash
import formulare as formulare
#from flask_cors import CORS
import pandas as pd
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func
 
# Initialize the Flask application
app = Flask(__name__)
#session key --------------------------------------- auf jedenfall noch anpassen
app.config['SECRET_KEY'] = 'mysecretkey'
#CORS(app)  # Aktiviere CORS für alle Routen
 
# Verbindung zur Datenbank herstellen
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scannerMarket.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#abc
db.init_app(app)
 
 
 
# Define the root route
@app.route('/')
def index():
    # Render the default template
    session['type'] = "default"
    return render_template('sm_cust_main.html')
 
# Define the route for the default page
# @app.route('/main')
# def defaultP():
#     return render_template('sm_cust_main.html')
 
@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = formulare.RegistrationForm()
    if form.validate_on_submit():
        # Hier Logik für die Registrierung hinzufügen
        flash('Registrierung erfolgreich!', 'success')
        session['type'] = 'customer'
        service.addNewCustomer(vorname=form.vorname.data, nachname=form.nachname.data, geb_datum=form.geburtsdatum.data, email=form.email.data, passwort=form.passwort.data, kundenkarte=form.kundenkarte.data, admin=False, newsletter=form.newsletter.data)
        customer = db.session.query('Nutzer').filter(Email=form.email.data)
        paying = db.session.query('Bezahlmöglichkeiten').filter(Methode=form.bezahlmethode.data)
        if form.bezahlmethode == 'paypal':
           payment= Bezahlung(customer.ID, paying.ID, PP_Email=form.paypal_email.data )
        else:
           payment= Bezahlung(customer.ID, paying.ID, Karten_Nr=form.kreditkarte_nummer.data, Karte_Gültigkeitsdatum=form.kreditkarte_gueltig_bis.data, Karte_Prüfnummer= form.kreditkarte_cvv.data )
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('productcatalog')) 
    return render_template('sm_registration.html', form=form)
 

@app.route('/login', methods=['GET', 'POST'])      
def login():
    form = formulare.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        ##hier checken, ob login Daten aus Formular in Datenbank und valide sind:    
        user = db.session.query(Nutzer).filter_by(Email=email, Passwort=password).first()
        if user: 
            ##wenn valide:
            session['logged_in'] = db.session.query(Nutzer).filter(Nutzer.Email == form.email) ## form.email ggfs anpassen
            customer =  session.get('logged_in', None)
            if customer.admin:
                session['type'] = "admin"
                return redirect(url_for('adminMain'))
            else:
                session['type'] = "customer"
                return redirect(url_for('productcatalog'))
        else:
             flash('Invalid username or password')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")
    return render_template('sm_login.html', form = form)
 
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
        join(Warenkorb.produkt).\
        filter(Warenkorb.Einkauf_ID == shopping_id).\
        options(joinedload(Warenkorb.produkt)).all()  # Lädt die Produktdaten vor, um N+1 Abfragen zu vermeiden
    
    for prod in prodsOfCategory:
        newProd = {'shoppingCard_id': prod.Einkauf_ID, 'product_id': prod.Produkt_ID,'name': prod.produkt.Name, 'amount': prod.Anzahl}
        products.append(newProd)
    print(products)
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
    dates = curr_Date()
    curr_month = dates["Monat"]
    curr_year = dates["Jahr"]

    #Umsatz vom aktuellen Monat
    salesOfCurrMonth=salesVolume_per_month( curr_year , curr_month)
    
    # Umsatz vom aktuellen Jahr
    salesOfCurrYear = 0
    for month in range(1, int(curr_month) + 1):
        salesOfCurrYear += salesVolume_per_month(curr_year, month)
    
    #am meisten gekaufte Produkte
    bestSellers = get_best_seller(curr_year, curr_month)
    bestSellers = [
        ("Apfel", "../static/images/category-frozen.jpg", 100),
        ("Birnen", "../static/images/category-meat.jpg", 10),
        ("Birnen", "../static/images/category-meat.jpg", 10)
    ]

    # monatsaktuelle Einkaufszahlen und wieviele Produkte verkauft wurden
    selledProds = numberOfSelledProducts(curr_year, curr_month)
    sells = numberOfSells(curr_year, curr_month)

    return render_template('umsatz.html', title="Umsatz", salesOfYear=salesOfCurrYear, 
                           salesOfMonth=salesOfCurrMonth, year=curr_year, month=dates["Monatsname"],
                           bestSellers=bestSellers, selledProds=selledProds, sells=sells)

#ChatGPT
def getStartEndDates(year, month):
    start= datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d')
    if int(month) == 12:
        end = start.replace(year= int(year)+1, month=1)
    else:
        end = start.replace(month=int(month)+1)
    return start, end

#ChatGPT
def salesVolume_per_month(year, month):
    start, end = getStartEndDates(year, month)
    salesVolume = db.session.query(func.sum(Produkte.Preis*Warenkorb.Anzahl)).join(Warenkorb).join(Einkauf).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).scalar() or 0
    return salesVolume

#ChatGPT
def get_best_seller(year,month):
    start, end = getStartEndDates(year, month)
    bestSeller = db.session.query(Produkte.Name, Produkte.Bild, func.sum(Warenkorb.Anzahl)).join(Warenkorb).join(Einkauf).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).group_by(Produkte.Name).order_by(func.sum(Warenkorb.Anzahl).desc()).limit(5).all() 
    if bestSeller is None:
        return (0,0,0)
    return bestSeller
#ChatGPT
def numberOfSelledProducts(year, month):
    start, end = getStartEndDates(year, month)
    number = db.session.query(func.sum(Warenkorb.Anzahl)).join(Einkauf).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).scalar() or 0  # or 0 sorgt dafür, dass falls die query keine Ergebnisse findet (None) ein Integer zurückgegeben wird
    return number
#ChatGPT
def numberOfSells(year, month):
    start, end = getStartEndDates(year, month)
    number = db.session.query(func.count(Einkauf.ID)).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).scalar() or 0 
    return number

    
#Funktion extrahiert die einzelnen Bestandteile des aktuellen Datums und gibt diese zurück
def curr_Date():
    curr_date= date.today()
    month_name= '{0:%B}'.format(curr_date) #Zahl des Monats zu englischen Klartext - bsp: 05 --> May
    curr_month= '{0:%m}'.format(curr_date) #nur Monatszahl mit ggfs. führender 0
    curr_year= '{0:%Y}'.format(curr_date) #nur Jahreszahl
    curr_day= '{0:%d}'.format(curr_date) #nur Tag mit ggfs. führender 0
    months={"January": "Januar", "February": "Februar", "March": "März", "April": "April", "May":"Mai", "June":"Juni", "July":"Juli", "August":"August", "September":"September","October":"Oktober","November":"November","December":"Dezember"}
   
    return {"Date":curr_date, "Monatsname":months[month_name], "Monat":curr_month, "Jahr":curr_year, "Tag":curr_day}

@app.route('/Neukunden')
def show_neukunden():
    dates = curr_Date()
    curr_month = dates["Monat"]
    curr_year = dates["Jahr"]
    month_name = dates["Monatsname"]
    start, end = getStartEndDates(curr_year, curr_month)
    newCust=db.session.query(func.count(Nutzer.ID)).filter(Nutzer.Registriert_am>= start, Nutzer.Registriert_am<= end).scalar() or 0
    allCust=db.session.query(func.count(Nutzer.ID)).scalar() or 0
    return render_template('neukunden.html',title = "Neukunden", month= month_name, newCust=newCust, allCust=allCust)
###########################################################################################################################################
#Formulare:
@app.route('/admin/newProduct', methods=['GET', 'POST'])
def newProduct():
    form = formulare.addProductForm()
   
    if form.validate_on_submit():
        session['newProduct'] = {
            'name' : form.name.data,
            'price' : str(form.price.data),
            'manufacturer' : form.manufacturer.data,
            'weight' : str(form.weight.data),
            'unit' : form.unit.data,
            'img' : form.img_url.data,
            'ean' : form.ean.data,
            'category_id' : str(form.category_ID.data)
        }
        return redirect(url_for('summeryNewProduct'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")
    return render_template('sm_admin_newProduct.html', form = form)

@app.route('/admin/summeryNewProduct')
def summeryNewProduct():
    product = session.get('newProduct', None)
    if not product:
        return redirect(url_for('newProduct'))

    #neues Product in die Datenbank hinzufügen
    gewicht = product['weight'] + ' ' + product['unit']
    product['weight'] = gewicht
    service.addNewProduct(hersteller=product['manufacturer'], produktname=product['name'], gewicht_volumen=gewicht, ean=product['ean'], preis=product['price'], bild=product['img'], kategorie=product['category_id'])
    return render_template('sm_admin_summeryProduct.html', product = product)



##################### besondere URLs/Funktionen:
 
@app.route('/insertDB')
def insertDB():
    # service.addNewCustomer(Vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='max.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am =date(2024,5,15)) 
    # service.addNewCustomer(vorname="Paulchen", nachname="Kleiner", geb_datum=date(1990, 1, 1), email='p.kleiner@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True)
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
 
    produkte_entries = db.session.query(Produkte).all()
    return render_template('produkte.html', produkte_entries=produkte_entries)
 
 
 
@app.route('/getProductFromEan', methods=["POST"])
def getProductFromEan():
    search_ean = request.args.get('ean')  # Use request.args for query parameters
    print(search_ean)
    produkte_entries = db.session.query(Produkte).filter_by(ean=search_ean).all()
    print(produkte_entries)
    return produkte_entries
 
 
# @app.route('/startOrEndShopping', methods=["GET", "POST"])
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
@app.route("/increase_cart_amount", methods=["POST"])
def increase_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    print(einkauf_id, produkt_id, " aus der empfangenen URL: /increase_cart_amount")
    response = Warenkorb.increase_cart_amount(einkauf_id, produkt_id)
    return response

@app.route("/decrease_cart_amount", methods=["POST"])
def decrease_cart_amount():
    einkauf_id = request.form["einkauf_id"]
    produkt_id = request.form["produkt_id"]
    print(einkauf_id, produkt_id, " aus der empfangenen URL: /decrease_cart_amount")
    response = Warenkorb.decrease_cart_amount(einkauf_id, produkt_id)
    return response

 
 
 
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