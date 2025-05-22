import tkinter as tk
import requests

API_KEY = "60971d0ec0cf350408c31a1aebbd77ae"  

def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("main"):
        temp = response["main"]["temp"]
        weather = response["weather"][0]["description"].title()
        result = f"Temperature in {city.title()}: {temp}°C\nCondition: {weather}"
        result_label.config(text=result)
    else:
        message = response.get("message", "Unknown error.")
        result_label.config(text=f"Error: {message.capitalize()}")

# Create GUI window
root = tk.Tk()
root.title("Weather App")
root.geometry("300x200")
resizable = (False, False)  # Disable resizing

# City input
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

# Search button
search_button = tk.Button(root, text="Get Weather", command=get_weather)
search_button.pack()

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=280, justify="center")
result_label.pack(pady=20)

# Run the app
root.mainloop()
