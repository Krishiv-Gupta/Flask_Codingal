from flask import Flask, render_template, request
import mysql.connector
import re

app = Flask(__name__)

@app.route('/details', methods=['POST', 'GET'])
def details():
    name = request.form['name']
    class1 = request.form['class']
    marks = request.form['marks']
    mydb = mysql.connector.connect(host="db4free.net",
                                    user="rootcodingal_123",
                                    password="root1234",
                                    database="students123")
    mycursor = mydb.cursor()
    mycursor.execute('INSERT INTO Student_Marks VALUES (%s, %s, %s)',(name, class1, marks))
    mydb.commit()
    return render_template('highestscorer.html')    
    
@app.route('/highestscorer', methods=['POST', 'GET'])
def highestcorer():
    mydb = mysql.connector.connect(host="db4free.net",
                                    user="rootcodingal_123",
                                    password="root1234",
                                    database="students123")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM Student_Marks WHERE Class = 10 ORDER BY Marks DESC')
    student = mycursor.fetchone()
    print(student)
    if student:
        name = student[0]
        class1 = student[1]
        marks = student[2]
        return render_template('highestscorer.html', name = name, class1 = class1, marks=marks)
    else:
        return render_template('highestscorer.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

