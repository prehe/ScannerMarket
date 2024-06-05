from flask import Blueprint, Flask, render_template, redirect, request, url_for, session, flash
from app_func import getTotalBasketPrice
import formulare as formulare
from model import db, Nutzer, Produktkategorien, Produkte, Einkauf, Warenkorb
from sqlalchemy.orm import joinedload
from flask import session

cust = Blueprint(__name__, import_name="app_cust")


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

# Methode zum Löschen von Flash-Nachrichten
def clear_flash_messages():
    session.pop('_flashes', None)

# REGISTRIERUNG & LOGIN
###########################################################################################################################################################################################
# Route zum Registrierungsformular
@cust.route('/registration', methods=['GET', 'POST'])
def registration():
    clear_flash_messages()
    form = formulare.RegistrationForm()
    if form.validate_on_submit():
        try:
            # Überprüfen, ob die Email schon in der Datenbank vorliegt
            if (db.session.query(Nutzer).filter(Nutzer.Email==form.email.data).first()):
                flash('die Email ist bereits vergeben', 'danger')
            elif (form.passwort.data != form.passwort_new.data): # überprüfen, ob das Passwort und die Passwortbestätigung gleich sind
                flash('Passwörter müssen übereinstimmen', 'danger')
            else: # Kunden hinzufügen
                customer = Nutzer.add_nutzer(vorname=form.vorname.data, nachname=form.nachname.data, geburtsdatum=form.geburtsdatum.data, email=form.email.data, passwort=form.passwort.data, kundenkarte=form.kundenkarte.data, admin=False, newsletter=form.newsletter.data)
                session['shoppingID'] = None
                session['userID'] = customer.ID  # Kunden-ID in session speichern 
                session['type'] = 'customer'     # Rolle in session speichern
                flash('Registrierung erfolgreich!', 'success')
                return redirect(url_for('app_customer.productcatalog'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    else: 
        for field, errors in form.errors.items(): # wenn validate_on_submit nicht funktioniert, wird der Fehler auf der Konsole ausgegeben
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")

    return render_template('sm_registration.html', form=form)
 
# Route zum Login-Formular
@cust.route('/login', methods=['GET', 'POST'])
def login():
    clear_flash_messages()
    form = formulare.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Überprüfen, ob Login-Daten zu einem registrierten Nutzer gehören
        user = db.session.query(Nutzer).filter_by(Email=email, Passwort=password).first()
        if user:
            session['shoppingID'] = None
            session['userID'] = user.ID  # Kunden-ID in session speichern
            customer = db.session.query(Nutzer).get(session['userID'])  # Fetch user instance

            # Rolle des angemeldeten Nutzers speichern und Weiterleitung anpassen
            if customer.Admin:
                session['type'] = "admin"
                return redirect(url_for('app_admin.adminMain'))
            else:
                session['type'] = "customer"
                return redirect(url_for('app_customer.productcatalog'))
        else:
            flash('Email oder Passwort falsch', 'warning')
    else:
        if request.method == 'POST':
            flash('Email oder Passwort falsch', 'warning')
    return render_template('sm_login.html', form=form)
        
            
# PRODUKTKATALOG & PRODUKTSEITEN
###########################################################################################################################################################################################
# Route zum Produktkatalog
@cust.route('/productcatalog')
def productcatalog():
    return render_template('sm_cust_main.html', logStatus = session.get('type', None))

# Route zur Kategorieseite
@cust.route("/category/<category>")
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
    products = getProdsFromCategory(categoryName) # alle Produkte der Kategorie aus der Datenbank ermitteln
    return render_template('sm_category_page.html', category= categoryName, products=products, banner= bannerImg,logStatus =session.get('type', None))
 
 # Methode zum ermitteln aller Produkte einer Kategorie - gibt Dictionary mit Produkten zurück
def getProdsFromCategory(category):
    products = []
    prodsOfCategory = db.session.query(Produkte).join(Produktkategorien).filter(Produktkategorien.Kategorie == category)
    for prod in prodsOfCategory:
        newProd = {'name': prod.Name, 'img': prod.Bild, 'weight' : prod.Gewicht_Volumen, 'price': prod.Preis, 'manufacturer' : prod.Hersteller}
        products.append(newProd)
    return products
 
 # EINKAUF & SCANNER
 ###########################################################################################################################################################################################
 # Route zur Einkaufsliste
@cust.route('/shoppinglist')
def shoppinglist():
    if session['shoppingID'] == None:
        session['shoppingID'] = Einkauf.add_einkauf(session.get('userID', None))
    data = getProdsFromShoppingList(session.get('shoppingID', None))
    return render_template('sm_shopping_list.html',  product_list = data[0], total_price=f"{data[1]:.2f}", logStatus = session.get('type', None), calling_page = 'shoppinglist')

# Route zum Scanner
@cust.route('/scanner')
def scanner():
    return render_template('sm_scanner.html', logStatus = session.get('type', None), calling_page = 'scanner')

# Route zur Einkauf-Beenden Seite
@cust.route('/shoppingresult')
def shoppingresult():
    return render_template('sm_shoppingresult.html', logStatus = session.get('type', None), calling_page = 'shoppingresult')

 # Ermittelt die Produktdaten der Einkaufsliste und berechnet den Gesamtpreis
def getProdsFromShoppingList(shopping_id):
    items = db.session.query(Warenkorb).\
    outerjoin(Warenkorb.einkauf).\
    join(Warenkorb.produkt).\
    filter(Warenkorb.Einkauf_ID == shopping_id).\
    options(joinedload(Warenkorb.produkt)).all()

    products = []
    for item in items:
        products.append({
            'shoppingCard_id': item.Einkauf_ID,
            'product_id': item.Produkt_ID,
            'hersteller': item.produkt.Hersteller,
            'name': item.produkt.Name,
            'amount': item.Anzahl,
            'price': item.produkt.Preis
        })
    total_price = getTotalBasketPrice(shopping_id)
    return products, total_price

# SONSTIGES: PROFIL, LOGOUT & IMPRESSUM
###########################################################################################################################################################################################

# Route zur Profilbearbeitung
@cust.route('/profile', methods=['GET', 'POST'])
def profile():
    clear_flash_messages()
    user = db.session.query(Nutzer).get(session['userID'])
    form = formulare.EditProfile(obj=user)
    if form.validate_on_submit():
        false_Entry = False

        # Überprüfen, ob die geänderte Email schon in der Datenbank existiert und ob diese zu einem anderen Nutzer gehört
        if (db.session.query(Nutzer).filter(Nutzer.ID != user.ID, Nutzer.Email==form.Email.data).first()):
            flash('die Email ist bereits vergeben', 'danger')
            false_Entry = True
        else:
            user.Email = form.Email.data

        # Überprüfen, ob das Datum geändert worden ist
        if form.Passwort.data:
            if form.Passwort.data == user.Passwort:                          # Überprüfen, ob das angegebene alte Passwort in der Datenbank beim Nutzer hinterlegt ist
                if form.Passwort_new.data:                                   # Überprüfen, ob ein neues Passwort angegeben ist
                    if  (form.Passwort_conf.data != form.Passwort_new.data): # Überprüfen, ob das neue Passwort mit dem Bestätigungsfeld übereinstimmt
                        flash('Felder "neues Passwort" und "Passwort bestätigen" müssen übereinstimmen', 'danger')
                        false_Entry = True
                    else: 
                        user.Passwort = form.Passwort_new.data
                else:
                    flash('kein neues Passwort angegeben - ihr altes Passwort wurde nicht verändert', 'danger')
                    false_Entry=True
            else:
                flash('die Eingabe des aktuellen Passwortes ist falsch', 'danger')   
                false_Entry=True

        # sonstige Änderungen übernehmen
        user.Vorname = form.Vorname.data
        user.Nachname = form.Nachname.data
        user.Geburtsdatum = form.Geburtsdatum.data
        user.Kundenkarte = form.Kundenkarte.data
        user.Newsletter = form.Newsletter.data
        db.session.commit()

        if false_Entry:  
            flash('nur fehlerfreie Änderungen wurden übernommen!', 'warning')
        else:
            flash('Änderung erfolgreich!', 'success')
    else:
        for field, errors in form.errors.items(): # falls validate_on_submit nicht funktioniert, wird ein Fehler auf der Console ausgegeben
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")
    return render_template('sm_profile.html',logStatus = session.get('type', None), form=form)


# Route für das Logout
@cust.route('/logout')
def logOut():
    session['type'] = "default"
    return redirect(url_for('app_customer.productcatalog'))


 # Route zum Impressum
@cust.route("/impressum")
def impressum ():
    return render_template('sm_impressum.html',logStatus =session.get('type', None))