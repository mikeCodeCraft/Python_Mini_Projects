import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    global generated_qr_img  # Store globally for save button
    data_type = qr_type_cb.get()
    user_data = text_entry.get()
    if not user_data:
        messagebox.showwarning("Input Error", "Please enter required data.")
        return

    # Format data based on type
    if data_type == "URL/Text":
        qr_data = user_data
    elif data_type == "WiFi Login":
        try:
            ssid, password = user_data.split(",", 1)
            qr_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter SSID and password separated by a comma.")
            return
    elif data_type == "Email":
        qr_data = f"mailto:{user_data}"
    elif data_type == "whatsapp":
        qr_data = f"https://wa.me/{user_data}"
    else:
        qr_data = user_data

    # Create QR
    qr = qrcode.QRCode(
        version=None,  # Automatic version sizing
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    fill_color = fg_color_var.get() or "black"
    back_color = bg_color_var.get() or "white"
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # Embed logo if available
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo_size = 60
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            qr_width, qr_height = qr_img.size
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
        except Exception as e:
            messagebox.showerror("Logo Error", f"Failed to embed logo: {e}")

    # Resize QR to fixed dimensions (e.g., 250x250 px)
    fixed_size = 250
    qr_img_resized = qr_img.resize((fixed_size, fixed_size), Image.LANCZOS)

    # Display QR
    qr_img_tk = ImageTk.PhotoImage(qr_img_resized)
    qr_label.config(image=qr_img_tk)
    qr_label.image = qr_img_tk

    generated_qr_img = qr_img  # Save original (high-res) image for saving

def upload_logo():
    global logo_path
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if path:
        logo_path = path
        logo_label.config(text=f"Logo selected ✔️")

def save_qr():
    if generated_qr_img is None:
        messagebox.showwarning("Save Error", "Please generate a QR code first.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if file_path:
        generated_qr_img.save(file_path)
        messagebox.showinfo("Saved", f"QR code saved as {file_path}")

def choose_fg_color():
    color = colorchooser.askcolor()[1]
    if color:
        fg_color_var.set(color)
        fg_color_label.config(text=f"FG: {color}")

def choose_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        bg_color_var.set(color)
        bg_color_label.config(text=f"BG: {color}")

#  GUI Setup 
root = tk.Tk()
root.title("Advanced QR Code Generator")
root.geometry("450x600")
root.resizable(False, False)

logo_path = None
generated_qr_img = None

# QR Type selection
tk.Label(root, text="QR Code Type:", font=("Arial", 12)).pack(pady=5)
qr_type_cb = tk.StringVar(value="URL/Text")
qr_type_menu = tk.OptionMenu(root, qr_type_cb, "URL/Text", "WiFi Login", "Email", "whatsapp")
qr_type_menu.config(font=("Arial", 12), width=20)
qr_type_menu.pack(pady=5)

# Data entry
tk.Label(root, text="Enter Data:", font=("Arial", 12)).pack(pady=5)
text_entry = tk.Entry(root, font=("Arial", 14), width=35)
text_entry.pack(pady=5)

# tk.Label(root, text="WiFi: SSID,Password  |  Email/Phone: Enter address only", fg="gray", font=("Arial", 9)).pack()

# Logo upload
tk.Button(root, text="Upload Logo (Optional)", command=upload_logo, bg="gray", fg="white").pack(pady=5)
logo_label = tk.Label(root, text="No logo selected", font=("Arial", 10), fg="blue")
logo_label.pack(pady=2)

# Color selectors
fg_color_var = tk.StringVar()
bg_color_var = tk.StringVar()

color_frame = tk.Frame(root)
color_frame.pack(pady=5)

tk.Button(color_frame, text="Choose FG Color", command=choose_fg_color, bg="black", fg="white").pack(side=tk.LEFT, padx=5)
fg_color_label = tk.Label(color_frame, text="FG: black", font=("Arial", 10))
fg_color_label.pack(side=tk.LEFT, padx=5)

tk.Button(color_frame, text="Choose BG Color", command=choose_bg_color, bg="white", fg="black").pack(side=tk.LEFT, padx=5)
bg_color_label = tk.Label(color_frame, text="BG: white", font=("Arial", 10))
bg_color_label.pack(side=tk.LEFT, padx=5)

# Generate + Save
tk.Button(root, text="Generate QR Code", command=generate_qr, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Save QR Code", command=save_qr, bg="blue", fg="white", font=("Arial", 12)).pack(pady=5)

qr_label = tk.Label(root)
qr_label.pack(pady=10)

root.mainloop() 