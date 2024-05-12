from model import db, Nutzer, Bezahlmöglichkeiten, Bezahlung, Produktkategorien, Produkte, Einkauf, Warenkorb

def getProductFromEAN(ean):
    product_data = db.session.query(Produkte).filter_by(ean=ean).all()

    print(product_data)