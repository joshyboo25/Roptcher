# ROPTCHER

**Rapid Operation Toolkit for Credential Hunting & Endpoint Reconnaissance**

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🚀 What is ROPTCHER?

ROPTCHER is a powerful and customizable command-line tool designed for ethical red teamers, security researchers, and advanced penetration testers.

It supports multithreaded brute-force authentication, CSRF-aware form submissions, runtime control, and more. Built for speed, modularity, and maximum operator control.

---

## 🔧 Features

* ✅ **Multithreaded login brute-force**
* 🔐 **CSRF token parsing and injection**
* ⏯️ **Runtime controls** (`CTRL+P` to pause, `CTRL+C` to stop cleanly)
* 📄 **Smart wordlist support** (filtered + customizable)
* 💡 **Minimal logging / visible output** for stealth testing

---

## 📦 Installation

```bash
# Clone the repo
$ git clone https://github.com/yourusername/roptcher.git
$ cd roptcher

# (Optional) Create a virtual environment
$ python -m venv venv
$ source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the tool
$ python roptcher.py --help
```

Dependencies are auto-installed on script execution. You can also run:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

```bash
python roptcher.py <url> <username> <wordlist.txt> [--threads N]
```

### Example:

```bash
python roptcher.py https://target.com/login admin passwords.txt --threads 10
```

### Arguments:

* `url` → The login endpoint URL
* `username` → The user to test against
* `wordlist.txt` → The file of passwords to iterate through
* `--threads` → (Optional) Number of threads (default is 5)

---

## 🧠 Tips for Wordlists

* Use your own `passwords.txt` or generate one with our `password_gen.py`.
* Combine dictionary words, symbols, numbers, and known info (OSINT).
* Ensure passwords meet the system’s length/policy requirements

---

## 🕵️ VPN & Stealthing Instructions

ROPTCHER **does not include proxy support**. To enhance anonymity and reduce detection:

* Use your own VPN for all sessions
* Activate **Multi-Hop VPN** (double-hop routing) for better operational security
* Avoid running attacks from your home IP — always route through secure, obfuscated networks
* Optional: combine with containerization or virtual machine setups

You are responsible for maintaining your own operational stealth.

---

## 🛑 Runtime Controls

* `CTRL+P` → Pause/resume the attack
* `CTRL+C` → Gracefully terminate threads and exit

---

## 📁 Output

* ✅ Found credentials are printed to console
* ❌ Failed attempts are logged with minimal noise
* Future releases will support export to `hits.txt`

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🧑‍💻 Credits

Crafted with ❤️ by Josh & ChatGPT
If you use this project or learn from it, consider giving credit or a ⭐ on GitHub.

---

## ⚠️ Legal Disclaimer

This project is for **educational and authorized security testing only**.
Unauthorized access or usage against systems you do not own or have explicit permission to test is illegal and unethical.
**You are fully responsible** for how you use this tool.


