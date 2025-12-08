from flask import Flask, render_template, request
import mysql.connector
import re

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/upload')
def upload_file():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
    
@app.route('/uploader', methods=['POST', 'GET'])
def uplaoder_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', msg='No file part')
        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', msg='No selected file')
        if file and allowed_file(file.filename):
            file.save(file.filename)
            return render_template('index.html', msg='file uploaded successfully')
        else:
            return render_template('index.html', msg='This file is not supported')
    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

