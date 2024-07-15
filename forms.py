from wtforms import Form, StringField, validators

class JobApplicationForm(Form):
    position = StringField('Position', [validators.DataRequired()])
    company = StringField('Company', [validators.DataRequired()])
