from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

def get_db_connection():
    return mysql.connector.connect(
        host="db4free.net",
        user="rootcodingal_123",
        password="root1234",
        database="students123"
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM BankManager WHERE Name = %s AND Password = %s', (username, password))
        account = mycursor.fetchone()
        mydb.close()
        
        if account:
            session['id'] = account[0]
            session['name'] = account[1]
            # Try to get balance from database, default to 12450.00 if not available
            try:
                session['balance'] = float(account[4]) if len(account) > 4 and account[4] is not None else 12450.00
            except:
                session['balance'] = 12450.00
            msg = 'Logged in Successfully'
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect Credentials. Kindly check again'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html', msg='')

@app.route('/dashboard')
def dashboard():

    
    # Get transactions for the user
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM Transactions WHERE user_id = %s ORDER BY date DESC LIMIT 10', (session['id'],))
    transactions = mycursor.fetchall()
    mydb.close()
    
    return render_template('index.html', 
                         name=session['name'], 
                         balance=session['balance'],
                         transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        action = data.get('action')
        description = data.get('description')
        amount = float(data.get('amount'))
        
        # Determine transaction type
        if action == 'Deposit':
            trans_type = 'Credit'
            session['balance'] += amount
        else:  # Send Money or Withdraw
            trans_type = 'Debit'
            session['balance'] -= amount
        
        # Save to database
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        
        # Create transactions table if it doesn't exist
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                date DATE,
                description VARCHAR(255),
                type VARCHAR(50),
                amount DECIMAL(10,2)
            )
        ''')
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        mycursor.execute(
            'INSERT INTO Transactions (user_id, date, description, type, amount) VALUES (%s, %s, %s, %s, %s)',
            (session['id'], date_str, description, trans_type, amount)
        )
        
        # Update user balance - check if Balance column exists
        try:
            mycursor.execute('UPDATE BankManager SET Balance = %s WHERE name = %s', (session['balance'], session['name']))
        except Exception as e:
            print(f"Balance update error: {e}")
            # Balance column might not exist, continue without updating
            pass
            
        mydb.commit()
        mydb.close()
        
        return jsonify({
            'success': True,
            'date': date_str,
            'description': description,
            'type': trans_type,
            'amount': amount,
            'new_balance': session['balance']
        })
    except Exception as e:
        print(f"Transaction error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM BankManager WHERE Name = %s', (name,))
        account = mycursor.fetchone()
        
        if account:
            msg = 'Account already exists'
            mydb.close()
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid Email Address'
            mydb.close()
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers'
            mydb.close()
        else:
            initial_balance = 12450.00
            # Check if Balance column exists, if not use the old table structure
            try:
                mycursor.execute('INSERT INTO BankManager (Name, Password, Email, Balance) VALUES (%s, %s, %s, %s)',
                               (name, password, email, initial_balance))
            except:
                # Fallback for old table structure without Balance column
                mycursor.execute('INSERT INTO BankManager (Name, Password, Email) VALUES (%s, %s, %s)',
                               (name, password, email))
            mydb.commit()
            user_id = mycursor.lastrowid
            mydb.close()
            
            session['id'] = user_id
            session['name'] = name
            session['balance'] = initial_balance
            msg = 'Your Registration is successful'
            return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        msg = 'Kindly fill the details'
    
    return render_template('registration.html', msg=msg)

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)