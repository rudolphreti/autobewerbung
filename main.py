import json
from create_application_files import create_application_files

with open('data.json', 'r') as file:
    job_applications = json.load(file)

for application in job_applications:
    create_application_files(application)
