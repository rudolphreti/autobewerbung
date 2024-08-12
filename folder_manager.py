import os
import shutil
import sys

def delete_folder_contents(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

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

def get_absolute_path(file_name):
    # Get the absolute path of the current directory (support for PyInstaller)
    current_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, file_name)

def sanitize_directory_name(name):
    # Replace invalid characters with underscores or other safe characters
    invalid_chars = ['/', '|', ':', '?', '<', '>', '*', '\\', '\n']
    for char in invalid_chars:
        name = name.replace(char, '_')
    if len(name) > 100:
        name = name[:100]  # Truncate the name if it exceeds 100 characters
    return name

def copy_applications_files(userAssetsDirectory, full_path, name):
    cv_zeugnis_source = os.path.join(userAssetsDirectory, 'CV_Zeugnis.pdf')
    cv_zeugnis_destination = os.path.join(full_path, f"CV_Zeugnis_{name}.pdf")
    shutil.copy(cv_zeugnis_source, cv_zeugnis_destination)
    
    profilphoto_source = os.path.join(userAssetsDirectory, 'profilfoto.jpg')
    profilphoto_destination = os.path.join(full_path, f"profilfoto_{name}.jpg")
    shutil.copy(profilphoto_source, profilphoto_destination)

    # Create a directory for separated CV and LAP-Zeugnis files if it doesn't exist
    cv_lap_separated_path = os.path.join(full_path, "CV_LAP_separated")
    os.makedirs(cv_lap_separated_path, exist_ok=True)

    # Copy the CV.pdf into the created directory CV_LAP_separated
    cv_source = os.path.join(userAssetsDirectory, 'CV.pdf')
    cv_destination = os.path.join(cv_lap_separated_path, f"CV_{name}.pdf")
    shutil.copy(cv_source, cv_destination)

    # Copy the LAP-Zeugnis.pdf into the created directory CV_LAP_separated
    zeugnis_source = os.path.join(userAssetsDirectory, 'LAP-Zeugnis.pdf')
    zeugnis_destination = os.path.join(cv_lap_separated_path, f"LAP-Zeugnis_{name}.pdf")
    shutil.copy(zeugnis_source, zeugnis_destination)