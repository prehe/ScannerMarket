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

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
    
# Liveserver nicht mehr möglich mit den child templates
# app.py ausführen mit STRG+C stoppen und mit dem folgenden Befehl dauerhaft laufen lassen 
# python -m flask --app app.py run --debug
# dann muss nur die Seite aktualiesiert werden und nicht immer app.py neu gestartet werden