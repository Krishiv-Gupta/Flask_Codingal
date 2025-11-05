from flask import Flask, render_template, request
import datetime
from dateutil import relativedelta

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def calculate():
    msg = ''
    if request.method == 'POST' and 'date1' in request.form and 'date2' in request.form:
        date1 = list(map(int, request.form.get('date1').split("-")))
        date2 = list(map(int, request.form.get('date2').split("-")))
        d1 = datetime.datetime(date1[0], date1[1], date1[2])
        d2 = datetime.datetime(date2[0], date2[1], date2[2])
        d = relativedelta.relativedelta(d2, d1)
        msg = str(d.years) + " years, " + str(d.months) + " months, " + str(d.days) + " days"

    return render_template('index.html', msg = msg)

@app.route('/')
def index():
    return render_template('index.html')


app.run(host = '0.0.0.0', port=8080)

