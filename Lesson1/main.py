from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def calculate():
    age = ''
    today = date.today()
    if request.method == 'POST' and 'born_year' in request.form:
        Born_year = int(request.form.get('born_year'))
        if Born_year>today.year:
            age = 'Invalid'
        else:
            age = today.year - Born_year
    return render_template('index.html', age = age)

@app.route('/')
def index():
    return render_template('index.html')


app.run(host = '0.0.0.0', port=8080)

