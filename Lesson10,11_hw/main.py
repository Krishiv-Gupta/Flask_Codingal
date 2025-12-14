from flask import Flask, render_template, request
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

otp = None

@app.route('/verify', methods=['POST'])
def verify():
    global otp
    email = request.form['email']
    
    otp = randint(100000, 999999)  
    
    msg = Message(
        subject='OTP Verification',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f"Your OTP is: {otp}"
    
    mail.send(msg)
    return render_template('page.html')

@app.route('/validate', methods=['POST'])
def validate():
    user_otp = request.form['otp']
    
    if otp is not None and int(user_otp) == otp:
        return render_template('main.html')
    else:
        return "<h3>Verification failed</h3>"

@app.route('/send', methods=['POST'])
def send():
    email = request.form['r_email']
    subject = request.form['subject']
    text = request.form['message']
    
    msg = Message(
        subject=subject,
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = text
    
    mail.send(msg)
    return render_template('main.html', sent=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
