import json
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from wtforms import Form, StringField, validators
from create_application_files import create_application_files
import webbrowser

app = Flask(__name__)
app.secret_key = 'secret'

class JobApplicationForm(Form):
    position = StringField('Position', [validators.DataRequired()])
    company = StringField('Company', [validators.DataRequired()])

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    job_applications = load_data()
    form = JobApplicationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_application = {
            "position": form.position.data,
            "company": form.company.data
        }
        job_applications.append(new_application)
        save_data(job_applications)
        create_application_files(new_application)  # Call the function here
        return redirect(url_for('index'))
    df = pd.DataFrame(job_applications)
    table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('index.html', table=table_html, form=form)


if __name__ == '__main__':
    job_applications = load_data()
    for application in job_applications:
        create_application_files(application)
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
