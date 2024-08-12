import os
import argparse
from flask import Flask
from flask_wtf import CSRFProtect
import webbrowser
from views import index, delete_application, update_field, main_bp
from data_manager import load_data, clear_data
from create_application_files import create_application_files
from folder_manager import delete_folder_contents
from unterlagen_update import regenerate_bp

app = Flask(__name__)
app.secret_key = 'secret'
csrf = CSRFProtect(app) 
app.register_blueprint(main_bp)
app.register_blueprint(regenerate_bp) 
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/delete/<int:index>', 'delete_application', delete_application, methods=['POST'])
app.add_url_rule('/update_field', 'update_field', update_field, methods=['POST'])

parser = argparse.ArgumentParser()
parser.add_argument('--rb', action='store_true', help='Delete all contents in the application folder')
parser.add_argument('--frb', action='store_true', help='Delete all contents in the application folder and clear all data')
args = parser.parse_args()

if __name__ == '__main__':
    if args.rb:
        delete_folder_contents(os.path.abspath('Bewerbungsunterlagen'))
    
    if args.frb:
        delete_folder_contents(os.path.abspath('Bewerbungsunterlagen'))
        clear_data()

    job_applications = load_data()
    for application in job_applications:
        create_application_files(application)
    
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)