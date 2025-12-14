from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators

class ContactForm(Form):
    name = StringField("Candidate Name", [validators.DataRequired("Please enter your name.")])
    Gender = RadioField("Gender", choices = [('M', 'Male'), ('F', 'Female')])
    Address = TextAreaField("Address")
    Age = IntegerField("Age")
    # langauge = SelectField('Programming Languages', choices = [('java', 'Java'), ('py', 'Python')])
    submit = SubmitField("Submit")

