import os
from File_organizer import FILE_CATEGORIES, move_file_to_category
import time

def auto_cleanup(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if ext in extensions:
                    move_file_to_category(file_path, path, category)
                    moved = True
                    break
            if not moved:
                move_file_to_category(file_path, path, "Others")

if __name__ == "__main__":
    folder = "C:/Users/YourName/Downloads"  # change this to your target folder
    auto_cleanup(folder)
