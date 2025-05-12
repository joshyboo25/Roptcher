# password_gen.py
from itertools import product

# 🔧 Customize this list
keywords = ["summer", "nicole", "stanly193", "2020", "Dixon", "snapchat", "gymnastics" "may6"]
symbols = ["_", "!", "@", "#", "$" "?" "%" "*" "&" "=" "+" "-"]
numbers = ["", "2006", "321", "1", "12", "1234", "06" "21" "22" "23" "24" "20" "19"]

# 💾 Output file
with open("password.txt", "w") as f:
    for base in keywords:
        for sym, num in product(symbols, numbers):
            pwd = f"{base}{sym}{num}"
            if 8 <= len(pwd) <= 16:  # Control password length
                f.write(pwd + "\n")

print("✅ Custom passwords.txt generated!")
