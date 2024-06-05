# app.py
from flask import Flask, render_template,  session
from model import db
from app_customer import cust
from app_admin import admin
from app_func import func
import os
import certifi
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector
import pymysql

 
# Initialize the Flask application
app = Flask(__name__)
app.register_blueprint(cust)
app.register_blueprint(admin)
app.register_blueprint(func)


# Initialize the Flask application
app.config['SECRET_KEY'] = 'mysecretkey'

# Set up Cloud SQL Connector
connector = Connector()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Function to get Cloud SQL connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "test1-424109:europe-west3:scannermarket-db-1",
        "pymysql",
        user="scanner",
        password="scanner",
        database="scannermarket-db-1",
    )
    return conn

# Configure Flask-SQLAlchemy to use Cloud SQL Connector
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

#############################################################################################



 
# Define the root route
@app.route('/')
def index():
    session['type'] = "default"
    return render_template('sm_cust_main.html', logStatus=session.get('type', None))
 

# Flask starten
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# app.py ausführen mit STRG+C stoppen und mit dem folgenden Befehl dauerhaft laufen lassen
