from flask import render_template, request, redirect, url_for, flash, request, jsonify
import pandas as pd
from forms import JobApplicationForm
from data_manager import load_data, save_data
from create_application_files import create_application_files
from flask import Blueprint


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    job_applications = load_data()
    form = JobApplicationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_application = {
            "position": form.position.data,
            "company": form.company.data,
            "URL": form.URL.data 
        }
        job_applications.append(new_application)
        save_data(job_applications)
        create_application_files(new_application)  # Call the function here
        return redirect(url_for('index'))
    df = pd.DataFrame(job_applications)
    table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('index.html', table=table_html, form=form, job_applications=job_applications)
pass

@main_bp.route('/delete/<int:index>', methods=['POST'])
def delete_application(index):
    job_applications = load_data()
    try:
        del job_applications[index]
        save_data(job_applications)
        flash('Application deleted successfully!', 'success')
    except IndexError:
        flash('Invalid application index!', 'danger')
    return redirect(url_for('index'))
pass



@main_bp.route('/update_field', methods=['POST'])
def update_field():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging-Ausgabe
        index = int(data.get('index'))  # Przekonwertuj na liczbę całkowitą
        field = data.get('field')
        value = data.get('value')

        if field is None or value is None:
            print("Missing data error")  # Debugging-Ausgabe
            return jsonify({'status': 'error', 'message': 'Missing data'}), 400

        # Lade die Daten und aktualisiere das entsprechende Feld
        job_applications = load_data()
        if index < len(job_applications):
            job_applications[index][field] = value
            save_data(job_applications)
            print("Field updated successfully")  # Debugging-Ausgabe
            return jsonify({'status': 'success'}), 200
        else:
            print("Invalid index error")  # Debugging-Ausgabe
            return jsonify({'status': 'error', 'message': 'Invalid index'}), 400
    except ValueError:
        print("Index is not a valid integer")  # Debugging-Ausgabe
        return jsonify({'status': 'error', 'message': 'Index is not a valid integer'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred'}), 500
pass