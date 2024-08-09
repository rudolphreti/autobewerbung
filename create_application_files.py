import os
import shutil
import sys
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.units import cm
from datetime import datetime

def sanitize_directory_name(name):
    # Replace invalid characters with underscores or other safe characters
    invalid_chars = ['/', '|', ':', '?', '<', '>', '*', '\\', '\n']
    for char in invalid_chars:
        name = name.replace(char, '_')
    if len(name) > 100:
        name = name[:100]  # Truncate the name if it exceeds 100 characters
    return name


def get_absolute_path(file_name):
    # Get the absolute path of the current directory (support for PyInstaller)
    current_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, file_name)

# Define the PDF generator function
def create_application_files(application):
    base_directory = get_absolute_path("Bewerbungsunterlagen")
    
    company_name = sanitize_directory_name(application['company'].replace(' ', '_'))
    position_name = sanitize_directory_name(application['position'].replace(' ', '_'))
    directory_name = f"{company_name}_{position_name}"
    
    full_path = os.path.join(base_directory, directory_name)
    os.makedirs(full_path, exist_ok=True) 

    pdf_file_path = os.path.join(full_path, f"Bewerbungsschreiben_Mikolaj_Kosmalski.pdf")
    doc = SimpleDocTemplate(pdf_file_path, pagesize=A4,
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=1*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Helvetica', fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='Header', fontName='Helvetica', fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='AlignRight', alignment=TA_RIGHT, fontName='Helvetica', fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='AlignCenterTitle', alignment=TA_CENTER, fontName='Helvetica-Bold', fontSize=16, leading=16))

    elements = []

    elements.append(Paragraph('Mikolaj Kosmalski', styles['Header']))
    elements.append(Paragraph('Pogrelzstraße 55/6/4', styles['Header']))
    elements.append(Paragraph('1220 Wien', styles['Header']))
    elements.append(Paragraph('<a href="mailto:mikolaj.jakub.kosmalski@gmail.com" color="blue"><u>mikolaj.jakub.kosmalski@gmail.com</u></a>', styles['Header']))
    elements.append(Paragraph('<a href="https://linkedin.com/in/mikolajkosmalski" color="blue"><u>linkedin.com/in/mikolajkosmalski</u></a>', styles['Header']))
    elements.append(Paragraph('0660 20 57 157', styles['Header']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('An:', styles['Header']))
    elements.append(Paragraph(application['company'], styles['Header']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f'Wien, {datetime.now().strftime("%d.%m.%Y")}', styles['AlignRight']))
    elements.append(Spacer(1, 40))
    if application["position"] == "Initiativbewerbung":
        elements.append(Paragraph(f'<b>{application["position"]}</b>', styles['AlignCenterTitle']))
    else:
        elements.append(Paragraph(f'<b>Bewerbung als {application["position"]}</b>', styles['AlignCenterTitle']))
    elements.append(Spacer(1, 40)) 
    
    position = application['position']
    company = application['company']

    if position == "Initiativbewerbung":
        text = f"bei {company}. "
    else:
        text = f"um die Position {position} bei {company}. "
    
    content = (
        "Sehr geehrte Damen und Herren,<br/><br/>"
        f"mit großer Begeisterung bewerbe ich mich {text}"
        "Ich habe gerade eine zweijährige Ausbildung im Bereich der Anwendungsentwicklung mit LAP abgeschlossen, wo ich solide Grundlagen in der objektorientierten Programmierung mit .NET/C# erlernte. Darüber hinaus bin ich in der Lage, Webanwendungen in ASP.NET mit REST API zu entwickeln, wobei ich SQL-Datenbanken effektiv nutze.<br/><br/>"
        
        "Von 2020 bis 2023 war ich Mitbegründer des Start-ups " '<a href="https://timagio.com" color="blue"><u>timagio.com</u></a>, '"das Apps für Eltern und Lehrer im Zusammenhang mit der Montessori-Pädagogik entwickelt. Dort habe ich mehrere Prototypen in JavaScript, Automatisierungen in Python und Powershell-Skripte entwickelt sowie Erfahrung mit Scrum, Azure DevOps und Git gesammelt.<br/><br/>"
        
        "Ich lerne schnell, habe einen analytischen Verstand, bin kreativ, offen für Kritik und resistent gegen Stress. Ich bin daher überzeugt, dass ich ein wertvolles Mitglied Ihres Teams sein kann. Ich freue mich darauf, in einem persönlichen Gespräch mehr über diese Position zu erfahren.<br/><br/>"
        
        "Um meine Einarbeitung zu erleichtern, bin ich gerne bereit ein Praktikum zu absolvieren. Sie könnten profitieren von einer Eingliederungsbeihilfe: <br/>"'<a href="https://ams.at/unternehmen/service-zur-personalsuche/foerderungen/eingliederungsbeihilfe" color="blue"><u>ams.at/unternehmen/service-zur-personalsuche/foerderungen/eingliederungsbeihilfe</u></a>.<br/><br/>'
        
        "Ich füge diesem Schreiben meinen Lebenslauf und meine LAP-Zeugnis bei.<br/><br/>"
        
        "Mit freundlichen Grüßen<br/>Mikolaj Kosmalski"
    )

    elements.append(Paragraph(content, styles['Justify']))
    
    doc.build(elements)
    
    # Copy additional files
    # get_absolute_path
    cv_zeugnis_source = get_absolute_path('CV_Zeugnis.pdf')
    cv_zeugnis_destination = os.path.join(full_path, f"CV_Zeugnis_Mikolaj_Kosmalski.pdf")
    shutil.copy(cv_zeugnis_source, cv_zeugnis_destination)
    
    profilphoto_source = get_absolute_path('profilfoto.jpg')
    profilphoto_destination = os.path.join(full_path, f"profilfoto_Mikolaj_Kosmalski.jpg")
    shutil.copy(profilphoto_source, profilphoto_destination)

    # Create a directory for separated CV and LAP-Zeugnis files if it doesn't exist
    cv_lap_separated_path = os.path.join(full_path, "CV_LAP_separated")
    os.makedirs(cv_lap_separated_path, exist_ok=True)

    # Copy the CV.pdf into the created directory CV_LAP_separated
    cv_source = get_absolute_path('CV.pdf')
    cv_destination = os.path.join(cv_lap_separated_path, f"CV_Mikolaj_Kosmalski.pdf")
    shutil.copy(cv_source, cv_destination)

    # Copy the LAP-Zeugnis.pdf into the created directory CV_LAP_separated
    zeugnis_source = get_absolute_path('LAP-Zeugnis.pdf')
    zeugnis_destination = os.path.join(cv_lap_separated_path, f"LAP-Zeugnis_Mikolaj_Kosmalski.pdf")
    shutil.copy(zeugnis_source, zeugnis_destination)


