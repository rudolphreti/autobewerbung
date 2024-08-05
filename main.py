import os
import shutil
import argparse
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
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--rb', action='store_true', help='Delete all contents in the application folder')
args = parser.parse_args()

def delete_folder_contents(folder_path):
    # Überprüfen, ob der Pfad existiert
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Versuchen, alle Inhalte im Verzeichnis zu löschen
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted folder: {item_path}")
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {str(e)}")

if __name__ == '__main__':
    if args.rb:
        # Absoluten Pfad zum Ordner "Bewerbungsunterlagen" einstellen
        delete_folder_contents(os.path.abspath('Bewerbungsunterlagen'))
    
    job_applications = load_data()
    for application in job_applications:
        create_application_files(application)
    
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
