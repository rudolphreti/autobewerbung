from flask import render_template, request, redirect, url_for
import pandas as pd
from forms import JobApplicationForm
from data_manager import load_data, save_data
from create_application_files import create_application_files

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
