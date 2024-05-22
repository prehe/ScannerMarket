# app.py
from flask import Flask, render_template,  session
from model import db
from app_customer import cust
from app_admin import admin
from app_func import func

 
# Initialize the Flask application
app = Flask(__name__)
app.register_blueprint(cust)
app.register_blueprint(admin)
app.register_blueprint(func)


#session key --------------------------------------- auf jedenfall noch anpassen
app.config['SECRET_KEY'] = 'mysecretkey' 

# Verbindung zur Datenbank herstellen
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scannerMarket.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 
 
# Define the root route
@app.route('/')
def index():
    # Render the default template
    session['type'] = "default"
    return render_template('sm_cust_main.html')
 
 


# Run the Flask application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
   
# Liveserver nicht mehr möglich mit den child templates
# app.py ausführen mit STRG+C stoppen und mit dem folgenden Befehl dauerhaft laufen lassen
# python -m flask --app app.py run --debug
# dann muss nur die Seite aktualiesiert werden und nicht immer app.py neu gestartet werden