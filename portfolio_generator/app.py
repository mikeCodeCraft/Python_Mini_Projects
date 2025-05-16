import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import os

def generate_website():
    name = name_entry.get()
    bio = bio_text.get("1.0", tk.END).strip()
    projects = projects_text.get("1.0", tk.END).strip()
    email = email_entry.get()
    phone = phone_entry.get()

    if not name or not bio or not email:
        messagebox.showwarning("Missing Info", "Please fill at least Name, Bio and Email.")
        return

    # Load template.html content
    with open("portfolio_generator/template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholders
    html_content = template.replace("{{name}}", name)\
                           .replace("{{bio}}", bio)\
                           .replace("{{projects}}", projects)\
                           .replace("{{email}}", email)\
                           .replace("{{phone}}", phone)

    # Ask where to save HTML file
    save_path = filedialog.asksaveasfilename(defaultextension=".html",
                                              filetypes=[("HTML files", "*.html")],
                                              title="Save Portfolio As")
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Copy CSS file into same folder as saved HTML
        css_dest = os.path.join(os.path.dirname(save_path), "portfolio_generator/style.css")
        with open("portfolio_generator/style.css", "r", encoding="utf-8") as css_src:
            with open(css_dest, "w", encoding="utf-8") as css_out:
                css_out.write(css_src.read())

        messagebox.showinfo("Success", f"Website saved to:\n{save_path}")
        webbrowser.open(f"file://{os.path.abspath(save_path)}")

# GUI setup
root = tk.Tk()
root.title("Portfolio Website Generator")
root.geometry("400x600")
root.resizable(False, False)

tk.Label(root, text="Name:", anchor="w").pack(fill="x")
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Bio:", anchor="w").pack(fill="x")
bio_text = tk.Text(root, height=5, font=("Arial", 12))
bio_text.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Projects:", anchor="w").pack(fill="x")
projects_text = tk.Text(root, height=5, font=("Arial", 12))
projects_text.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Email:", anchor="w").pack(fill="x")
email_entry = tk.Entry(root, font=("Arial", 12))
email_entry.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Phone:", anchor="w").pack(fill="x")
phone_entry = tk.Entry(root, font=("Arial", 12))
phone_entry.pack(fill="x", padx=10, pady=5)

tk.Button(root, text="Generate Portfolio Website", command=generate_website, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

root.mainloop()
