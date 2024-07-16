import json
import os

def get_data_file_path():
    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path to data.json
    return os.path.join(current_dir, 'data.json')

def load_data():
    data_file_path = get_data_file_path()
    with open(data_file_path, 'r') as file:
        return json.load(file)

def save_data(data):
    data_file_path = get_data_file_path()
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=4)
