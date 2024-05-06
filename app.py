from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sm_cust_main.html')

@app.route('/templates/sm_cust_main.html')
def defaultP():
    return render_template('sm_cust_main.html')

@app.route('/templates/sm_registration.html')
def registrationP():
    return render_template('sm_registration.html')

@app.route('/templates/nwm_login.html')
def loginP():
    return render_template('nwm_login.html')

if __name__ == '__main__':
    app.run(debug=True)