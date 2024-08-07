import json
import os

def get_data_file_path():
    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path to data.json
    return os.path.join(current_dir, 'data.json')

def load_data():
    data_file_path = get_data_file_path()
    with open(data_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data):
    data_file_path = get_data_file_path()
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def clear_data():
    # Get the path to the data file
    data_file_path = get_data_file_path()
    # Open the data file in write mode and empty its contents to an empty list
    with open(data_file_path, 'w') as file:
        json.dump([], file, indent=4)
