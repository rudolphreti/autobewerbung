def generate_application_content(company, position, user_data):
    # Dynamisch den Bewerbungstext basierend auf der Position erstellen
    if position == "Initiativbewerbung":
        position_text = f"bei {company}. "
    else:
        position_text = f"um die Position {position} bei {company}. "
    
    # Aufbau des vollständigen Inhalts aus user_data
    content = (
        user_data['application_text']['introduction'] +
        user_data['application_text']['position_intro'] + position_text +
        user_data['application_text']['education'] +
        user_data['application_text']['experience'] +
        user_data['application_text']['skills'] +
        user_data['application_text']['internship_offer'] +
        user_data['application_text']['closing']
    )
    
    return content