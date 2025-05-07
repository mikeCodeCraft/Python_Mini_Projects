import tkinter as tk
import webbrowser as wb
import os

def webauto():
    chrome_path = r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    
    # Registering Chrome browser
    wb.register('chrome', None, wb.BackgroundBrowser(chrome_path))
    url = "https://www.google.com/?authuser=0"
   
    # this are the links that will be opened when the program is run
    URLS = (
        'https://chat.openai.com/auth/login?amp=1', # opens my chatgpt
        'https://www.udemy.com/course/', # Opens my udemy courses
        'https://www.youtube.com/@mikecodecraft', # opens my youtube channel
        'https://www.linkedin.com/in/michael-okon-774399244/',# Opens my LinkedIn profile
        'https://www.github.com/michaelokon', # Opens my github profile 
        'https://web.facebook.com/', # Opens facebook
        'https://x.com/mikeCodeCraft' # Opens my x profile
    )
    
    for url in URLS:
        print(f'Opening {url}')
        wb.get('chrome').open(url)
    
webauto()   
# root = tk.Tk()
# root.title("Auto browse")
# root.geometry("200x200")
# root.resizable(False, False)
        
# label = tk.Label(root, text = "Click here to open your\n favourite web pages", font=("Arial", 12))
# label.pack(pady=30)

# btn_file = tk.Button(root, text="Open", command=webauto)
# btn_file.pack(pady=5)


# root.mainloop()