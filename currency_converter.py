import tkinter as tk
from tkinter import ttk
import requests

# Enter your CurrencyLayer API key here
API_KEY = "Go to CurrencyLayer API to get it"

# List of available currencies
CURRENCIES = [
    "USD", "NGN", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY", "ZAR", "GHS", "KES",
    "INR", "BRL", "MXN", "CHF"
]

def convert_currency():
    amount = amount_entry.get()
    from_currency = from_currency_cb.get()
    to_currency = to_currency_cb.get()

    if not amount or not from_currency or not to_currency:
        result_label.config(text="Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        result_label.config(text="Amount must be a number.")
        return

    mikeCodeCraft = f"http://api.currencylayer.com/convert?access_key={API_KEY}&from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(mikeCodeCraft).json()

    if response.get("success") and response.get("result"):
        result = response["result"]
        result_label.config(text=f"{amount} {from_currency} = {result:.2f} {to_currency}")
    else:
        error_info = response.get("error", {}).get("info", "Unknown error")
        result_label.config(text=f"Error: {error_info}")

# Build GUI
root = tk.Tk()
root.title("Currency Converter mikeCodeCraft")
root.geometry("400x300")
root.resizable(False, False)

# Amount input
tk.Label(root, text="Amount:", font=("Arial", 12)).pack(pady=5)
amount_entry = tk.Entry(root, font=("Arial", 14))
amount_entry.pack(pady=5)

# From Currency dropdown
tk.Label(root, text="From Currency:", font=("Arial", 12)).pack(pady=5)
from_currency_cb = ttk.Combobox(root, values=CURRENCIES, font=("Arial", 12), state="readonly")
from_currency_cb.set("USD")  # Default value
from_currency_cb.pack(pady=5)

# To Currency dropdown
tk.Label(root, text="To Currency:", font=("Arial", 12)).pack(pady=5)
to_currency_cb = ttk.Combobox(root, values=CURRENCIES, font=("Arial", 12), state="readonly")
to_currency_cb.set("NGN")  # Default value
to_currency_cb.pack(pady=5)

# Convert Button
convert_btn = tk.Button(root, text="Convert", command=convert_currency, font=("Arial", 12), bg="blue", fg="white")
convert_btn.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=380, justify="center")
result_label.pack(pady=10)

root.mainloop()
