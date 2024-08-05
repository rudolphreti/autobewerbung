import os
import shutil

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
