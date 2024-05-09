from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

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

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
    
# Liveserver nicht mehr möglich mit den child templates
# app.py ausführen mit STRG+C stoppen und mit dem folgenden Befehl dauerhaft laufen lassen 
# python -m flask --app app.py run --debug
# dann muss nur die Seite aktualiesiert werden und nicht immer app.py neu gestartet werden
