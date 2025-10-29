from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def calculate():
    msg = ''
    if request.method == 'POST' and 'year' in request.form:
        year = int(request.form.get('year'))
        if year%4==0 and year%400!=0:
            msg = f'{year} is a Leap year'
        else:
            msg = f'{year} is not a Leap year'
    return render_template('index.html', msg = msg)

@app.route('/')
def index():
    return render_template('index.html')


app.run(host = '0.0.0.0', port=8080)

