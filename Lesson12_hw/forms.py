from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators

class CollegeForm(Form):
    name = StringField("Candidate Name", [validators.DataRequired("Please enter your name.")])
    Gender = RadioField("Gender", choices = [('M', 'Male'), ('F', 'Female')])
    Address = TextAreaField("Address")
    Age = IntegerField("Age")
    Subject = SelectField('Subject', choices = ['Engineering', 'Medical', 'Economics'])
    submit = SubmitField("Submit")

