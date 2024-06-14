from flask import Blueprint, Flask, render_template, session, redirect, url_for
import formulare as formulare
from model import db, Nutzer, Produktkategorien, Produkte, Einkauf, Warenkorb
import db_service as service
from datetime import date, datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func


admin = Blueprint(__name__, import_name="app_admin")
 
 # Route zur Übersichtsseite des Administrators
@admin.route('/admin')
def adminMain():
    return render_template('sm_admin_main.html',logStatus =session.get('type', None))
 
 # Route zur Übersichtsseite der Analysen des Administrators
@admin.route('/admin/analysis')
def analysis():
    return render_template('sm_admin_analysis.html', analyse_page= "/Produktkategorien",logStatus =session.get('type', None))

###########################################################################################################################################
# Route zur Kundendatenbankseite
@admin.route('/Kunden')
def show_nutzer():
    nutzer_entries = db.session.query(Nutzer).all()
    column_names = ["ID", "Vorname", "Nachname", "Geburtsdatum", "Email", "Passwort", "Kundenkarte", "Admin", "Newsletter", "Registriert_am"]
    return render_template('sm_admin_table_view.html', entries=nutzer_entries, column_names=column_names, title = "registrierte Kunden")
 
 # Route zur Produktkategoriendatenbankseite
@admin.route('/Produktkategorien')
def show_produktkategorie():
    produktkategorien_entries = db.session.query(Produktkategorien).all()
    column_names = ["ID", "Kategorie"]
    return render_template('sm_admin_table_view.html',entries=produktkategorien_entries, column_names= column_names, title = "Produktkategorien")
 
 # Route zur Produktdatenbank
@admin.route('/Produkte')
def show_produkte():
    #Alle Produkte aus der Excel-Tabelle in die Datenbank einfügen
    # service.addAllProductsFromExcel(categoryNames)  
    produkte_entries = db.session.query(Produkte).all()
    column_names = ["ID", "Hersteller", "Name", "Gewicht_Volumen", "EAN", "Preis","Bild", "Kategorie_ID"]
    return render_template('sm_admin_table_view.html', entries=produkte_entries, column_names= column_names, title = "Produkte")
 
 # Route zur Einkaufsdatenbank
@admin.route('/Einkauf')
def show_einkauf():
    einkauf_entries = db.session.query(Einkauf).all()
    column_names =["ID", "Nutzer_ID",  "Zeitstempel_start","Zeitstempel_ende" ]
    return render_template('sm_admin_table_view.html', entries=einkauf_entries, column_names=column_names, title = "Einkauf")
 
 # Route zur Warenkorbdatenbank
@admin.route('/Warenkorb')
def show_warenkorb():
    warenkorb_entries = db.session.query(Warenkorb).all()
    column_names = ["Einkauf_ID", "Produkt_ID", "Anzahl"]
    return render_template('sm_admin_table_view.html', entries=warenkorb_entries, column_names=column_names, title = "Warenkorb")
 
 # Route zur Analysenseite
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
    
    if bestSellers == []:
        bestSellers = [
            ("Apfel", "../static/images/category-frozen.jpg", 100),
            ("Birnen", "../static/images/category-meat.jpg", 10),
            ("Birnen", "../static/images/category-meat.jpg", 10)
        ]

    # monatsaktuelle Einkaufszahlen und wieviele Produkte verkauft wurden
    selledProds = numberOfSelledProducts(curr_year, curr_month)
    sells = numberOfSells(curr_year, curr_month)

    # Kundendaten abfragen
    start, end = getStartEndDates(curr_year, curr_month)
    newCust=db.session.query(func.count(Nutzer.ID)).filter(Nutzer.Registriert_am>= start, Nutzer.Registriert_am<= end).scalar() or 0
    allCust=db.session.query(func.count(Nutzer.ID)).scalar() or 0
   
    return render_template('sm_admin_umsatz.html', salesOfYear=salesOfCurrYear, 
                           salesOfMonth=salesOfCurrMonth, year=curr_year, month=dates["Monatsname"],
                           bestSellers=bestSellers, selledProds=selledProds, sells=sells,newCust=newCust, allCust=allCust)

#ChatGPT
# liefert die Start- und End-Daten des angegebenen Monats
def getStartEndDates(year, month):
    start= datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d')
    if int(month) == 12:
        end = start.replace(year= int(year)+1, month=1)
    else:
        end = start.replace(month=int(month)+1)
    return start, end

#ChatGPT
# liefert den monatlichen Umsatz
def salesVolume_per_month(year, month):
    start, end = getStartEndDates(year, month)
    salesVolume = db.session.query(func.round(func.sum(Produkte.Preis*Warenkorb.Anzahl), 2)).join(Warenkorb).join(Einkauf).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).scalar() or 0
    return salesVolume

#ChatGPT
# liefert die 5 bestverkauftetsten Produkte
def get_best_seller(year,month):
    start, end = getStartEndDates(year, month)
    bestSeller = db.session.query(Produkte.Name, Produkte.Bild, func.sum(Warenkorb.Anzahl)).join(Warenkorb).join(Einkauf).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).group_by(Produkte.Name, Produkte.Bild).order_by(func.sum(Warenkorb.Anzahl).desc()).limit(5).all() 
    if bestSeller is None:
        return []
    return bestSeller

#ChatGPT
# liefert die Anzahl der insgesamt verkauften Produkte des Monats
def numberOfSelledProducts(year, month):
    start, end = getStartEndDates(year, month)
    number = db.session.query(func.sum(Warenkorb.Anzahl)).join(Einkauf).filter(Einkauf.Zeitstempel_ende>= start, Einkauf.Zeitstempel_ende<= end).scalar() or 0  # or 0 sorgt dafür, dass falls die query keine Ergebnisse findet (None) ein Integer zurückgegeben wird
    return number

#ChatGPT
# liefert die Anzahl der Einkäufe des Monats
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


###########################################################################################################################################
# Formular zum hinzufügen eines Produktes - Verwaltung, Datenbankänderung + Weiterleitung
@admin.route('/admin/newProduct', methods=['GET', 'POST'])
def newProduct():
    form = formulare.addProductForm()
   
    # Eingaben validieren und in Session speichern --> Weiterleitung an Zusammenfassungsseite
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
        for field, errors in form.errors.items(): # falls es Fehler bei validate_on_submit gibt, wird dieser auf der Console ausgegeben
            for error in errors:
                print(f"Fehler im Feld '{getattr(form, field).label.text}': {error}")

    return render_template('sm_admin_newProduct.html', form = form)

# Zusammenfassungsseite des neuhinzugefügten Produktes
@admin.route('/admin/summeryNewProduct')
def summeryNewProduct():
    product = session.get('newProduct', None)
    if not product:
        return redirect(url_for('newProduct'))

    #neues Product in die Datenbank hinzufügen
    gewicht = product['weight'] + ' ' + product['unit']
    product['weight'] = gewicht
    service.addNewProduct(hersteller=product['manufacturer'], produktname=product['name'], gewicht_volumen=gewicht, ean=product['ean'], preis=product['price'], bild=product['img'], kategorie=product['category_id'])
    return render_template('sm_admin_summeryProduct.html', product = product)