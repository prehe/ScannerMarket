from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, session, flash
import formulare as formulare
import pandas as pd
import requests
from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func


admin = Blueprint(__name__, import_name="app_admin")


#dürfen nur einsehbar sein, wenn eingelogter Nutzer ein Administrator ist

@admin.route('/admin')
def adminMain():
    return render_template('sm_admin_main.html',logStatus=session.get('type', None))
 
@admin.route('/admin/analysis')
def analysis():
    return render_template('sm_admin_analysis.html',logStatus=session.get('type', None))


@admin.route('/Kunden')
def show_nutzer():
    #Kunden hinzufügen
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='ma.musn@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am= date(2024, 5, 14))
    #service.addNewCustomer(vorname="Peter", nachname="Muster", geb_datum=date(1990, 1, 1), email='peter.muster@example.com', passwort='geheim', kundenkarte=True, admin=False, newsletter=True, reg_am =date(2024,5,15))
   
    nutzer_entries = db.session.query(Nutzer).all()
    # print(nutzer_entries[0].ID)
    column_names = ["ID", "Vorname", "Nachname", "Geburtsdatum", "Email", "Passwort", "Kundenkarte", "Admin", "Newsletter", " Registriert_am"]
    return render_template('db_table_view.html', entries=nutzer_entries, column_names=column_names, title = "registrierte Kunden")
 
@admin.route('/Produktkategorien')
def show_produktkategorie():
    #Produktkategorien zur Datenbank einmalig hinzufügen
    #service.addProductCategories(categoryNames)
 
    produktkategorien_entries = db.session.query(Produktkategorien).all()
    column_names = ["ID", "Kategorie"]
    return render_template('db_table_view.html',entries=produktkategorien_entries, column_names= column_names, title = "Produktkategorien")
 
@admin.route('/Produkte')
def show_produkte():
    #Alle Produkte aus der Excel-Tabelle in die Datenbank einfügen
    # service.addAllProductsFromExcel(categoryNames)  
    produkte_entries = db.session.query(Produkte).all()
    column_names = ["ID", "Hersteller", "Name", "Gewicht_Volumen", "EAN", "Preis","Bild", "Kategorie_ID"]
    return render_template('db_table_view.html', entries=produkte_entries, column_names= column_names, title = "Produkte")
 
 
####ToDo: auf Tabellenanzeige Template anpassen
@admin.route('/Einkauf')
def show_einkauf():
    einkauf_entries = db.session.query(Einkauf).all()
    column_names =["ID", "Nutzer_ID",  "Zeitstempel_start","Zeitstempel_ende" ]
    return render_template('db_table_view.html', entries=einkauf_entries, column_names=column_names, title = "Einkauf")
 
@admin.route('/Warenkorb')
def show_warenkorb():
    warenkorb_entries = db.session.query(Warenkorb).all()
    column_names = ["Einkauf_ID", "Produkt_ID", "Anzahl"]
    return render_template('db_table_view.html', entries=warenkorb_entries, column_names=column_names, title = "Warenkorb")
 
@admin.route('/Bezahlmöglichkeiten')
def show_bezahlmöglichkeiten():
    bezahlmoeglichkeiten_entries = db.session.query(Bezahlmöglichkeiten).all()
    column_names = ["ID", "Methode"]
    return render_template('db_table_view.html', entries=bezahlmoeglichkeiten_entries, column_names=column_names, title="Bezahlmöglichkeiten")
 
@admin.route('/Bezahlung')
def show_bezahlung():
    bezahlung_entries = db.session.query(Bezahlung).all()
    column_names = ["Nutzer_ID", "Bezahlmöglichkeiten_ID", "PP_Email", "Karten_Nr", "Karte_Gültingkeitsdatum", "Karte_Prüfnummer" ]
    return render_template('db_table_view.html', entries =bezahlung_entries, column_names=column_names, title = "Bezahlung")

 


@admin.route('/Umsatz')
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

@admin.route('/Neukunden')
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
@admin.route('/admin/newProduct', methods=['GET', 'POST'])
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
    return render_template('sm_admin_newProduct.html', form = form,logStatus=session.get('type', None))

@admin.route('/admin/summeryNewProduct')
def summeryNewProduct():
    product = session.get('newProduct', None)
    if not product:
        return redirect(url_for('newProduct'))

    #neues Product in die Datenbank hinzufügen
    gewicht = product['weight'] + ' ' + product['unit']
    product['weight'] = gewicht
    service.addNewProduct(hersteller=product['manufacturer'], produktname=product['name'], gewicht_volumen=gewicht, ean=product['ean'], preis=product['price'], bild=product['img'], kategorie=product['category_id'])
    return render_template('sm_admin_summeryProduct.html', product = product,logStatus=session.get('type', None))