from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, session, flash
import formulare as formulare
import pandas as pd
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func

cust = Blueprint(__name__, import_name="app_cust")


@cust.route('/registration', methods=['GET', 'POST'])
def registration():
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
        return redirect(url_for('app_customer.productcatalog')) 
    return render_template('sm_registration.html', form=form)
 

@cust.route('/login', methods=['GET', 'POST'])      
def login():
    form = formulare.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        ##hier checken, ob login Daten aus Formular in Datenbank und valide sind:    
        user = db.session.query(Nutzer).filter_by(Email=email, Passwort=password).first()
        if user: 
            ##wenn valide:
            if user.Admin:
                session['type'] = "admin"
                return redirect(url_for('app_admin.adminMain'))
            else:
                session['type'] = "customer"
                return redirect(url_for('app_customer.productcatalog'))
        else:
             flash('Invalid username or password')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")
    return render_template('sm_login.html', form = form)
 
@cust.route('/scanner')
def scannerP():
    return render_template('sm_scanner.html',logStatus=session.get('type', None))
 
@cust.route('/shoppinglist')
def prodBasketP():
    return render_template('sm_shopping_list.html', product_list = getProdsFromShoppingList(1),logStatus=session.get('type', None))
 
@cust.route('/productcatalog')
def productcatalog():
    return render_template('sm_cust_main.html',logStatus=session.get('type', None))

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
    products = getProdsFromCategory(categoryName)
    return render_template('sm_category_page.html', category= categoryName, products=products, banner= bannerImg,logStatus=session.get('type', None))
 
 
def getProdsFromCategory(category):
    products = []
    prodsOfCategory = db.session.query(Produkte).join(Produktkategorien).filter(Produktkategorien.Kategorie == category)
    for prod in prodsOfCategory:
        newProd = {'name': prod.Name, 'img': prod.Bild, 'weight' : prod.Gewicht_Volumen, 'price': prod.Preis, 'manufacturer' : prod.Hersteller}
        products.append(newProd)
    return products
 
@cust.route("/impressum")
def impressum ():
    return render_template('sm_impressum.html',logStatus=session.get('type', None))
 
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

@cust.route("/logout")
def logout ():
    session['type'] = "default"
    return redirect(url_for('app_customer.productcatalog'))