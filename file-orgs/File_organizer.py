import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# Category: Extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".odt"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json"],
    "Installers": [".exe", ".msi", ".dmg", ".deb"],
}


def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        list_files(folder_selected)

def list_files(path):
    files_listbox.delete(0, tk.END)  # Clear listbox
    try:
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                files_listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list files:\n{e}")
import shutil

def organize_files():
    path = folder_path.get()
    if not path:
        messagebox.showwarning("No Folder", "Please select a folder first.")
        return

    moved_files = {}

    try:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                moved = False

                for category, extensions in FILE_CATEGORIES.items():
                    if file_ext in extensions:
                        new_path = move_file_to_category(file_path, path, category)
                        moved_files[new_path] = file_path  # log: new → old
                        moved = True
                        break

                if not moved:
                    new_path = move_file_to_category(file_path, path, "Others")
                    moved_files[new_path] = file_path

        # Save undo log
        with open("organizer_log.json", "w") as f:
            json.dump(moved_files, f)

        messagebox.showinfo("Success", "Files have been organized!")
        list_files(path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to organize files:\n{e}")

    path = folder_path.get()
    if not path:
        messagebox.showwarning("No Folder", "Please select a folder first.")
        return

    try:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                moved = False

                for category, extensions in FILE_CATEGORIES.items():
                    if file_ext in extensions:
                        move_file_to_category(file_path, path, category)
                        moved = True
                        break

                if not moved:
                    move_file_to_category(file_path, path, "Others")

        messagebox.showinfo("Success", "Files have been organized!")
        list_files(path)  # Refresh the file list
    except Exception as e:
        messagebox.showerror("Error", f"Failed to organize files:\n{e}")

def move_file_to_category(file_path, base_path, category):
    category_path = os.path.join(base_path, category)
    os.makedirs(category_path, exist_ok=True)
    new_path = os.path.join(category_path, os.path.basename(file_path))
    shutil.move(file_path, new_path)
    return new_path

def undo_organize():
    if not os.path.exists("organizer_log.json"):
        messagebox.showinfo("Nothing to Undo", "No organization log found.")
        return

    try:
        with open("organizer_log.json", "r") as f:
            moved_files = json.load(f)

        for src, dest in moved_files.items():
            if os.path.exists(src):
                shutil.move(src, dest)

        os.remove("organizer_log.json")
        messagebox.showinfo("Undo Complete", "Files moved back successfully.")
        list_files(folder_path.get())

    except Exception as e:
        messagebox.showerror("Error", f"Undo failed:\n{e}")


# --- GUI Setup ---
root = tk.Tk()
root.title("File Organizer")
root.geometry("500x400")

folder_path = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Selected Folder:").pack()
tk.Entry(frame, textvariable=folder_path, width=60).pack(pady=5)
tk.Button(frame, text="Browse Folder", command=select_folder).pack(pady=5)
tk.Button(frame, text="Organize Files", command=organize_files).pack(pady=5)
tk.Button(frame, text="Undo Last Organize", command=undo_organize).pack(pady=5)

tk.Label(root, text="Files in Folder:").pack()
files_listbox = tk.Listbox(root, width=60, height=15)
files_listbox.pack(pady=10)

root.mainloop()
