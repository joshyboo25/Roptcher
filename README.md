# Roptcher 🛠️ - Multi-threaded Login Brute Forcer

Roptcher is a multi-threaded, visually styled brute-forcing utility designed to test login endpoints that use a 2-step login flow (like `username → password` on separate pages). It is ideal for educational, auditing, or red teaming use cases. **It does not use proxies**, so VPN or multihop usage is strongly advised.

---

## 📌 Features
- Multi-threaded brute forcing (`--threads` support)
- Keyboard controls: pause/resume with `CTRL+P`, quit instantly with `CTRL+C`
- Styled console output (with emoji fallback)
- Custom wordlist support
- Auto-handles CSRF/XSRF and AI tokens
- Logs successful credentials to `hits.txt`
- Saves last server response to `last_response.html` for debugging

---

## ⚙️ Usage
### 🔧 Requirements
Ensure Python 3.x is installed. Roptcher auto-installs dependencies:
- `requests`
- `beautifulsoup4`
- `colorama`
- `keyboard`

> ⚠️ On Windows, `keyboard` may require admin privileges to function correctly.

### ▶️ Launch Command
```bash
python Roptcherv1.1.py <login_url> <username> <wordlist.txt> --threads 5
```

#### Example:
```bash
python Roptcherv1.1.py https://accounts.example.com/accounts/v2/login jayleigh_w21 wordlist.txt --threads 5
```

---

## 🔐 How It Works
1. Connects to the login page with the target username.
2. Base64-encodes the username to generate the `ai_token`.
3. Extracts `xsrf_token` from cookies.
4. Sends a POST to `/accounts/v2/password?ai=<token>` with the password.
5. Checks if the final redirect is `/accounts/welcome` or if login succeeded.
6. If success, logs to `hits.txt`. If not, moves to next password.

---

## 🛡️ Recommended Precautions
- **Use a VPN**, proxy, or Tor to mask activity. This script does not use built-in proxy rotation.
- Enable **multihop** on VPN for added stealth.
- Respect terms of service and laws in your country. This tool is intended for testing **only with permission**.

---

## 📂 Output Files
- `hits.txt` → Stores any successful logins.
- `last_response.html` → Stores the latest server response for inspection.

---

## 🧠 Author
Built by **@joshyboo25** with lots of thc and caffeine ☕ — have fun guys just be carful and please remember i am not responsible for your stupidity.

---

## 📄 License
MIT License — free to use, modify, and distribute.


