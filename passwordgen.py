import string
import random

def passwordgen(length):
    password = ''
    for i in range(length):
        password += random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)
    print(password)
    
length = int(input("enter your password length: "))

passwordgen(length)
    