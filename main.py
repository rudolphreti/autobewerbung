import os
import argparse
from flask import Flask
from flask_wtf import CSRFProtect
import webbrowser
from views import index, delete_application
from data_manager import load_data, clear_data
from create_application_files import create_application_files
from folder_manager import delete_folder_contents

app = Flask(__name__)
app.secret_key = 'secret'
csrf = CSRFProtect(app)  # CSRF-Schutz aktivieren

app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/delete/<int:index>', 'delete_application', delete_application, methods=['POST'])
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--rb', action='store_true', help='Delete all contents in the application folder')
parser.add_argument('--frb', action='store_true', help='Delete all contents in the application folder and clear all data')
args = parser.parse_args()

if __name__ == '__main__':
    if args.rb:
        # Absoluten Pfad zum Ordner "Bewerbungsunterlagen" einstellen
        delete_folder_contents(os.path.abspath('Bewerbungsunterlagen'))
    
    if args.frb:
            # Absoluten Pfad zum Ordner "Bewerbungsunterlagen" einstellen und Daten löschen
            delete_folder_contents(os.path.abspath('Bewerbungsunterlagen'))
            clear_data()

    job_applications = load_data()
    for application in job_applications:
        create_application_files(application)
    
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)