from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class JobApplicationForm(FlaskForm):
    company = StringField('Company')
    position = StringField('Position')
    submit = SubmitField('Add Application')
