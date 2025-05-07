import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image

def process_image(input_file, output_file):
   
    image = Image.open(input_file)
    result = remove(image)
    result.save(output_file)
    result.show()


def handle_input(path):
    if os.path.isdir(path):
        files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not files:
            messagebox.showinfo("No images", "No image files found in folder.")
            return
        for file in files:
            input_file = os.path.join(path, file)
            filename_wo_ext = os.path.splitext(file)[0]
            output_file = os.path.join(path, f"{filename_wo_ext}_no_bg.png")
            process_image(input_file, output_file)
    elif os.path.isfile(path):
        filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
        output_file = os.path.join(os.path.dirname(path), f"{filename_wo_ext}_no_bg.png")
        process_image(path, output_file)
    else:
        messagebox.showwarning("Invalid Input", "Please drop a valid file or folder.")

def browse_files():
    path = filedialog.askopenfilename(title="Select Image")
    if path:
        handle_input(path)

def browse_folder():
    path = filedialog.askdirectory(title="Select Folder")
    if path:
        handle_input(path)

def on_drop(event):
    path = event.data.strip('{}')  # Handles Windows path formatting
    handle_input(path)

# --- GUI Setup ---
root = tk.Tk()
root.title("Background Remover")
root.geometry("400x200")
root.resizable(False, False)

label = tk.Label(root, text="Drag & drop a file/folder here\nor use the buttons below", font=("Arial", 12))
label.pack(pady=30)

btn_file = tk.Button(root, text="Choose Image", command=browse_files)
btn_file.pack(pady=5)

btn_folder = tk.Button(root, text="Choose Folder", command=browse_folder)
btn_folder.pack(pady=5)

# Drag-and-drop support on Windows/macOS with tkinterdnd2
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    root.destroy()  # Recreate root with DnD support
    root = TkinterDnD.Tk()
    root.title("Background Remover")
    root.geometry("400x200")
    root.resizable(False, False)

    label = tk.Label(root, text="Drag & drop a file/folder here\nor use the buttons below", font=("Arial", 12))
    label.pack(pady=30)

    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', on_drop)

    btn_file = tk.Button(root, text="Choose Image", command=browse_files)
    btn_file.pack(pady=5)

    btn_folder = tk.Button(root, text="Choose Folder", command=browse_folder)
    btn_folder.pack(pady=5)

except ImportError:
    print("🛑 Drag-and-drop support requires tkinterdnd2.\nInstall it via pip: pip install tkinterdnd2")
    


credit = tk.Label(root, text="Created by mikeCodeCraft", font=("Arial", 10))
credit.pack(pady=5)



root.mainloop()
