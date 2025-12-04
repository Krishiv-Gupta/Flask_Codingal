from flask import Flask, render_template, request
import mysql.connector
import re

app = Flask(__name__)

@app.route('/details', methods=['POST', 'GET'])
def details():
    user_name = request.form['user_name']
    phone_number = request.form['contact_number']
    number_of_items = request.form['number_of_items']
    total_amount = request.form['amount']
    current_date = request.form['current_date']
    mydb = mysql.connector.connect(host="db4free.net",
                                    user="rootcodingal_123",
                                    password="root1234",
                                    database="students123")
    mycursor = mydb.cursor()
    mycursor.execute('INSERT INTO Customer_Details VALUES (%s, %s, %s, %s, %s)',(user_name, phone_number, number_of_items, total_amount, current_date))
    mydb.commit()
    return render_template('winner.html')    
    
@app.route('/winner', methods=['POST', 'GET'])
def winner():
    mydb = mysql.connector.connect(host="db4free.net",
                                    user="rootcodingal_123",
                                    password="root1234",
                                    database="students123")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM Customer_Details WHERE Date_of_Purchase = CURRENT_DATE ORDER BY Total_Amount DESC')
    account = mycursor.fetchone()
    print(account)
    if account:
        user_name = account[0]
        phone_number = account[1]
        return render_template('winner.html', user_name = user_name, phone_number = phone_number)
    else:
        return render_template('winner.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

