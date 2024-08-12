import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.units import cm
from folder_manager import get_absolute_path, sanitize_directory_name, copy_applications_files
from letter_content import generate_application_content

with open('settings.json', 'r', encoding='utf-8') as file:
    settings = json.load(file)

userAssetsDirectory = get_absolute_path(settings['userAssetsDirectory'])
user_json_path = get_absolute_path(f"{userAssetsDirectory}/user.json") 

with open(user_json_path, 'r', encoding='utf-8') as file:
    user_data = json.load(file)

# Define the PDF generator function
def create_application_files(application):
    base_directory = get_absolute_path("Bewerbungsunterlagen")
    
    company_name = sanitize_directory_name(application['company'].replace(' ', '_'))
    position_name = sanitize_directory_name(application['position'].replace(' ', '_'))
    directory_name = f"{company_name}_{position_name}"
    
    full_path = os.path.join(base_directory, directory_name)
    os.makedirs(full_path, exist_ok=True) 

    pdf_file_path = os.path.join(full_path, f"Bewerbungsschreiben_{user_data['name'].replace(' ', '_')}.pdf")
    doc = SimpleDocTemplate(pdf_file_path, pagesize=A4,
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=1*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Helvetica', fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='Header', fontName='Helvetica', fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='AlignRight', alignment=TA_RIGHT, fontName='Helvetica', fontSize=12, leading=16))
    styles.add(ParagraphStyle(name='AlignCenterTitle', alignment=TA_CENTER, fontName='Helvetica-Bold', fontSize=16, leading=16))

    elements = []

    # Add user details from JSON
    elements.append(Paragraph(user_data['name'], styles['Header']))
    elements.append(Paragraph(user_data['address'], styles['Header']))
    elements.append(Paragraph(user_data['zip_code'] + " " + user_data['city'], styles['Header']))
    elements.append(Paragraph(f'<a href="mailto:{user_data["email"]}" color="blue"><u>{user_data["email"]}</u></a>', styles['Header']))
    elements.append(Paragraph(f'<a href="{user_data["linkedin"]}" color="blue"><u>{user_data["linkedin"]}</u></a>', styles['Header']))
    elements.append(Paragraph(user_data['phone'], styles['Header']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('An:', styles['Header']))
    elements.append(Paragraph(application['company'], styles['Header']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f'{user_data["city"]}, {datetime.now().strftime("%d.%m.%Y")}', styles['AlignRight']))
    elements.append(Spacer(1, 40))
    
    # Add application position details
    if application["position"] == "Initiativbewerbung":
        elements.append(Paragraph(f'<b>{application["position"]}</b>', styles['AlignCenterTitle']))
    else:
        elements.append(Paragraph(f'<b>Bewerbung als {application["position"]}</b>', styles['AlignCenterTitle']))
    elements.append(Spacer(1, 40)) 
    
    # Build the application content
    position = application['position']
    company = application['company']
    
    content = generate_application_content(company, position, user_data)

    elements.append(Paragraph(content, styles['Justify']))
    
    doc.build(elements)
    
    # Copy other required application files
    copy_applications_files(userAssetsDirectory, full_path, user_data['name'].replace(' ', '_'))
