from flask import Flask
from flask_wtf import CSRFProtect
import webbrowser
from views import index, delete_application
from data_manager import load_data
from create_application_files import create_application_files

app = Flask(__name__)
app.secret_key = 'secret'
csrf = CSRFProtect(app)  # CSRF-Schutz aktivieren

app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/delete/<int:index>', 'delete_application', delete_application, methods=['POST'])

if __name__ == '__main__':
    job_applications = load_data()
    for application in job_applications:
        create_application_files(application)
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
