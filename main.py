import os
import shutil
import json
from fpdf import FPDF
from datetime import datetime
from pdf_generator import PDF, line_height, font_family  # Importujesz klasę PDF oraz zmienne konfiguracyjne


with open('data.json', 'r') as file:
    job_applications = json.load(file)

def create_application_files(application):
    base_directory = "Bewerbungsunterlagen"
    directory_name = f"{application['id']}_{application['company'].replace(' ', '_')}_{application['position'].replace(' ', '_')}"
    full_path = os.path.join(base_directory, directory_name)
    os.makedirs(full_path, exist_ok=True) 
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font(font_family, '', 12)
    pdf.cell(0, line_height, '', 0, 1)
    pdf.cell(0, line_height, 'An:', 0, 1)
    pdf.cell(0, line_height, application['company'], ln=1)
    pdf.cell(0, line_height, f'Wien, {datetime.now().strftime("%d.%m.%Y")}', align='R')
    pdf.ln(15)
    pdf.set_font(font_family, 'B', 14) 
    pdf.cell(0, line_height, f"Bewerbung als {application['position']}", align='C')
    pdf.set_font(font_family, '', 12)  
    pdf.ln(15)
    # Treść listu motywacyjnego
    pdf.write(line_height, "Sehr geehrte Damen und Herren,\n\nmit großer Begeisterung bewerbe ich mich um die Position" 
                         f"{application['position']} bei {application['company']}. Ich habe gerade eine zweijährige "
                         "Ausbildung im Bereich der Anwendungsentwicklung mit LAP abgeschlossen, wo ich solide Grundlagen "
                         "in der objektorientierten Programmierung mit .NET/C# erlernte. Darüber hinaus bin ich in der Lage, "
                         "Webanwendungen in ASP.NET zu entwickeln, wobei ich SQL-Datenbanken effektiv nutze.\n\n"
                         "Seit 2020 war ich bis 2023 als Mitbegründer im Startup ")

    # Dodanie linku timagio.com w tej samej linii
    pdf.set_text_color(0, 0, 255)
    pdf.set_font(font_family, 'U', 12)
    pdf.write(line_height, "timagio.com", "https://timagio.com")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_family, '', 12)
    pdf.write(line_height, ", das sich auf pädagogische Hilfsmittel für den polnischsprachigen Leseunterricht spezialisiert. "
                           "Dort habe ich mehrere Prototypen in JavaScript, Automatisierungen in Python und Powershell-Skripte entwickelt.\n\n")

    pdf.write(line_height, "Ich habe Erfahrung mit Azure DevOps, Git, Chat GPT und Github Copilot gesammelt. Den Einsatz von KI-Lösungen "
                         "sehe ich als unverzichtbar für die moderne Softwareentwicklung und meine berufliche Weiterbildung an.\n\n"
                         "Mit meiner Erfahrung und meinem Engagement für innovative Lösungen im IT-Bereich bin ich überzeugt, dass ich "
                         "einen wertvollen Beitrag zu Ihrem Team leisten kann. Ich freue mich darauf, in einem persönlichen Gespräch mehr "
                         "über diese Position zu erfahren.\n\n"
                         "Um meine Einarbeitung zu erleichtern, bin ich gerne bereit ein Praktikum zu absolvieren. Sie könnten profitieren "
                         "von einer Eingliederungsbeihilfe: ")

    # Dodanie linku ams.at w tej samej linii
    pdf.set_text_color(0, 0, 255)
    pdf.set_font(font_family, 'U', 12)
    pdf.write(line_height, "ams.at/unternehmen/service-zur-personalsuche/foerderungen/eingliederungsbeihilfe", 
              "https://ams.at/unternehmen/service-zur-personalsuche/foerderungen/eingliederungsbeihilfe")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_family, '', 12)
    pdf.write(line_height, ".\n\n")

    pdf.multi_cell(0, 7, "Ich füge diesem Schreiben meinen Lebenslauf und meine LAP-Zeugnis bei.\n\n"
                         "Mit freundlichen Grüßen\nMikolaj Kosmalski")
    
    pdf_file_path = os.path.join(full_path, f"Bewerbungsschreiben_Mikolaj Kosmalski_{application['company']}.pdf")
    pdf.output(pdf_file_path)

    # Copy the CV_Zeugniss.pdf into the created directory
    cv_zeugnis_destination = os.path.join(full_path, f"CV_Zeugniss_Mikolaj Kosmalski_{application['company']}.pdf")
    shutil.copy('CV_Zeugniss.pdf', cv_zeugnis_destination)

    # Copy the profilfoto.jpg into the created directory
    profilphoto_destination = os.path.join(full_path, f"profilfoto_Mikolaj Kosmalski_{application['company']}.jpg")
    shutil.copy('profilfoto.jpg', profilphoto_destination)

    # Create a directory for separated CV and LAP-Zeugnis files if it doesn't exist
    cv_lap_separated_path = os.path.join(full_path, "CV_LAP_separated")
    os.makedirs(cv_lap_separated_path, exist_ok=True)

    # Copy the CV.pdf into the created directory CV_LAP_separated"
    cv_source = 'CV.pdf'
    cv_destination = os.path.join(cv_lap_separated_path, f"CV_Mikolaj Kosmalski_{application['company']}.pdf")
    shutil.copy(cv_source, cv_destination)

    # Copy the LAP-Zeugnis.pdf into the created directory CV_LAP_separated"
    zeugnis_source = 'LAP-Zeugnis.pdf'
    zeugnis_destination = os.path.join(cv_lap_separated_path, f"LAP-Zeugnis_Mikolaj Kosmalski_{application['company']}.pdf")
    shutil.copy(zeugnis_source, zeugnis_destination)

for application in job_applications:
    create_application_files(application)
