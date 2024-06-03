from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, session, flash
from app_func import getTotalBasketPrice
import formulare as formulare
import pandas as pd
import requests
from model import db, Nutzer, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from flask import session

cust = Blueprint(__name__, import_name="app_cust")


def clear_flash_messages():
    session.pop('_flashes', None)

@cust.route('/registration', methods=['GET', 'POST'])
def registration():
    clear_flash_messages()
    form = formulare.RegistrationForm()
    if form.validate_on_submit():
        try:
            if (db.session.query(Nutzer).filter(Nutzer.Email==form.email.data).first()):
                flash('die Email ist bereits vergeben', 'danger')
            else:
                customer = Nutzer.add_nutzer(vorname=form.vorname.data, nachname=form.nachname.data, geburtsdatum=form.geburtsdatum.data, email=form.email.data, passwort=form.passwort.data, kundenkarte=form.kundenkarte.data, admin=False, newsletter=form.newsletter.data)
                session['shoppingID'] = None
                session['userID'] = customer.ID  # Store user ID in session
                flash('Registrierung erfolgreich!', 'success')
                session['type'] = 'customer'
                return redirect(url_for('app_customer.productcatalog'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")

    return render_template('sm_registration.html', form=form)
 

@cust.route('/login', methods=['GET', 'POST'])
def login():
    clear_flash_messages()
    form = formulare.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Check if login data from the form is valid in the database
        user = db.session.query(Nutzer).filter_by(Email=email, Passwort=password).first()
        if user:
            # If valid:
            session['shoppingID'] = None
            session['userID'] = user.ID  # Store user ID in session
            customer = db.session.query(Nutzer).get(session['userID'])  # Fetch user instance
            if customer.Admin:
                session['type'] = "admin"
                return redirect(url_for('app_admin.adminMain'))
            else:
                session['type'] = "customer"
                return redirect(url_for('app_customer.productcatalog'))
        else:
            flash('Email oder Passwort falsch', 'warning')
    return render_template('sm_login.html', form=form)


 
@cust.route('/shoppinglist')
def shoppinglist():
    if session['shoppingID'] == None:
        session['shoppingID'] = Einkauf.add_einkauf(session.get('userID', None))
    data = getProdsFromShoppingList(session.get('shoppingID', None))
    return render_template('sm_shopping_list.html',  product_list = data[0], total_price=f"{data[1]:.2f}", logStatus = session.get('type', None))

@cust.route('/scanner')
def scanner():
    return render_template('sm_scanner.html')

@cust.route('/shoppingresult')
def shoppingresult():
    return render_template('sm_shoppingresult.html')
 
@cust.route('/productcatalog')
def productcatalog():
    return render_template('sm_cust_main.html', logStatus = session.get('type', None))

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
    return render_template('sm_category_page.html', category= categoryName, products=products, banner= bannerImg,logStatus =session.get('type', None))
 
 
def getProdsFromCategory(category):
    products = []
    prodsOfCategory = db.session.query(Produkte).join(Produktkategorien).filter(Produktkategorien.Kategorie == category)
    for prod in prodsOfCategory:
        newProd = {'name': prod.Name, 'img': prod.Bild, 'weight' : prod.Gewicht_Volumen, 'price': prod.Preis, 'manufacturer' : prod.Hersteller}
        products.append(newProd)
    return products
 
@cust.route("/impressum")
def impressum ():
    return render_template('sm_impressum.html',logStatus =session.get('type', None))
 
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

@cust.route('/logout')
def logOut():
    session['type'] = "default"
    return redirect(url_for('app_customer.productcatalog'))

@cust.route('/profile', methods=['GET', 'POST'])
def profile():
    clear_flash_messages()
    user = db.session.query(Nutzer).get(session['userID'])
    form = formulare.EditProfile(obj=user)
    print(user.Vorname, user.Nachname, user.Email)
    if form.validate_on_submit():
        
        if (db.session.query(Nutzer).filter(Nutzer.ID != user.ID, Nutzer.Email==form.Email.data).first()):
            flash('die Email ist bereits vergeben', 'danger')
        else:
            user.Email = form.Email.data
        user.Vorname = form.Vorname.data
        print(form.Vorname.data)
        user.Nachname = form.Nachname.data
        user.Geburtsdatum = form.Geburtsdatum.data
        if form.Passwort.data:
            if form.Passwort.data == user.Passwort:
                if form.Passwort_new.data:
                    user.Passwort = form.Passwort_new.data
                else:
                    flash('kein neues Passwort angegeben', 'danger')
            else:
                flash('falsches Passwort', 'danger')   
        user.Kundenkarte = form.Kundenkarte.data
        user.Newsletter = form.Newsletter.data
        db.session.commit()
        flash('Änderung erfolgreich!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")
    return render_template('sm_profile.html',logStatus = session.get('type', None), form=form)