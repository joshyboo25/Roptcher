import os
from itertools import product

# 🔧 Custom keyword base
keywords = [
    "admin", "test", "user", "guest", "root",
    "access", "default", "login", "secure", "portal"
]

symbols = [
    "", "_", "!", "@", "#", "$", "?", "%", "*", "&", "=", "+", "-"
]

numbers = [
    "", "123", "2024", "2023", "001", "1234", "111", "000", "789", "999", "314", "007"
]

# 📁 Create 'passwords' folder if it doesn't exist
output_dir = os.path.join(os.path.dirname(__file__), "passwords")
os.makedirs(output_dir, exist_ok=True)

# 📝 Function to get a unique filename
def get_unique_filename(base_name="passwords.txt"):
    path = os.path.join(output_dir, base_name)
    if not os.path.exists(path):
        return path
    count = 1
    while True:
        alt_path = os.path.join(output_dir, f"passwords({count}).txt")
        if not os.path.exists(alt_path):
            return alt_path
        count += 1

# 🎯 Generate passwords
def generate_passwords():
    output_file = get_unique_filename()
    total = 0

    with open(output_file, "w") as f:
        for base in keywords:
            for sym, num in product(symbols, numbers):
                pwd = f"{base}{sym}{num}"
                if 8 <= len(pwd) <= 16:
                    f.write(pwd + "\n")
                    total += 1

    print(f"✅ Generated {total} passwords.")
    print(f"📁 Output file: {output_file}")

# 🚀 Run it
if __name__ == "__main__":
    generate_passwords()
