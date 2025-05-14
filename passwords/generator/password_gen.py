import os
from itertools import product

# 🔧 Custom keyword base
keywords = [
    "summer", "may", "nicole", "ToyotaTacoma", "heather",
    "Dixon", "letmein", "admin", "secure", "portal", "dance" 
]

numbers = [
    "2006", "06", "2024", "2023", "1996", "1234", "111", "0506", "789", "", "314", "6"
]

symbols = [
    "#", "_", "!", "@", "$", "?", "%", "*", "&", "=", "+", "-"
]

# 📁 Create 'passwords' folder if it doesn't exist
output_dir = os.path.join(os.path.dirname(__file__), "passwords")
os.makedirs(output_dir, exist_ok=True)

# 📝 Function to get a unique filename
def get_unique_filename(base_name="generated-pass.txt"):
    path = os.path.join(output_dir, base_name)
    if not os.path.exists(path):
        return path
    count = 1
    while True:
        alt_path = os.path.join(output_dir, f"generated-pass({count}).txt")
        if not os.path.exists(alt_path):
            return alt_path
        count += 1

# 🎯 Generate passwords (keyword + number + symbol)
def generate_passwords():
    output_file = get_unique_filename()
    total = 0

    with open(output_file, "w") as f:
        for base in keywords:
            for num, sym in product(numbers, symbols):
                pwd = f"{base}{num}{sym}"
                if 8 <= len(pwd) <= 16:
                    f.write(pwd + "\n")
                    total += 1

    print(f"✅ Generated {total} passwords.")
    print(f"📁 Output file: {output_file}")

# 🚀 Run it
if __name__ == "__main__":
    generate_passwords()
