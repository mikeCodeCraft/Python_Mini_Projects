def generate_qr():
    data_type = qr_type_cb.get()
    user_data = text_entry.get()
    if not user_data:
        messagebox.showwarning("Input Error", "Please enter required data.")
        return

    # Format data based on type
    if data_type == "URL/Text":
        qr_data = user_data
    elif data_type == "WiFi Login":
        ssid, password = user_data.split(",") if "," in user_data else (user_data, "")
        qr_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    elif data_type == "Email":
        qr_data = f"mailto:{user_data}"
    elif data_type == "Phone":
        qr_data = f"tel:{user_data}"
    else:
        qr_data = user_data

    # Create QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    print(f"QR Data: {qr_data}")
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

    # Display QR
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=qr_img_tk)
    qr_label.image = qr_img_tk
    qr_label.qr_image = qr_img

    # Copy image to clipboard automatically
    copy_image_to_clipboard(qr_img)

    messagebox.showinfo("Copied!", "QR code copied to clipboard!")