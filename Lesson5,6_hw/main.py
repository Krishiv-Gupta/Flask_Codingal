from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/resume" , methods=['POST' , 'GET'])
def resume():
	user_name = request.form['user_name']
	email_id = request.form['email_id']
	contact_number = request.form['contact_number']
	grade = request.form['grade']
	school_name = request.form['school_name']
	percentage = request.form['percentage']
	year = request.form['year']
	independent_course = request.form['independent_course']
	dob = request.form['dob']
	father_name = request.form['father_name']
	mother_name = request.form['mother_name']
	hobbies = request.form['hobbies']
	return render_template('resume_template.html',user_name=user_name,email_id=email_id,contact_number=contact_number, grade=grade,school_name=school_name,percentage=percentage,year=year, independent_course=independent_course,dob=dob,father_name=father_name,mother_name=mother_name, hobbies=hobbies)


@app.route('/')
def index():
	return render_template('index.html')

app.run(host='0.0.0.0', port=8080)