from flask import Blueprint, redirect, url_for
from data_manager import load_data
from create_application_files import create_application_files
from folder_manager import delete_folder_contents
import os

# Erstellen eines Blueprints für die neue Route
regenerate_bp = Blueprint('regenerate_bp', __name__)

@regenerate_bp.route('/regenerate', methods=['POST'])
def regenerate_applications():
    job_applications = load_data()  # Lade bestehende Bewerbungen
    delete_folder_contents(os.path.abspath('Bewerbungsunterlagen'))  # Lösche vorhandene Unterlagen
    for application in job_applications:
        create_application_files(application)  # Generiere alle Unterlagen neu
    return redirect(url_for('index'))  # Nach dem Neugenerieren zur Hauptseite zurückkehren
