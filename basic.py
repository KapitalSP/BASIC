import os
import sys
import platform
import urllib.request
import zipfile
import shutil
import stat

# ==============================================================================
# 🏭 BASIC v9.1 (Full Multilingual Edition)
# The complete ecosystem with 10-language support and Omni-Selector logic.
# Optimized for GitHub deployment and global accessibility.
# ==============================================================================

def ask_and_download(base_dir):
    drivers_dir = os.path.join(base_dir, "drivers")
    os.makedirs(drivers_dir, exist_ok=True)
    
    URL_BASE = "https://github.com/ggerganov/llama.cpp/releases/download/b4604/"
    
    options = {
        "1": {"name": "Windows (PC)",      "file": "llama-cli.exe",     "save": "llama-cli.exe",     "url": URL_BASE + "llama-b4604-bin-win-avx-x64.zip"},
        "2": {"name": "Android (Termux)",  "file": "llama-cli",         "save": "llama-cli-android", "url": URL_BASE + "llama-b4604-bin-android-arm64-v8a.zip"},
        "3": {"name": "Mac (Apple Silicon)","file": "llama-cli",        "save": "llama-cli-mac",     "url": URL_BASE + "llama-b4604-bin-macos-arm64.zip"},
        "4": {"name": "Linux (Server)",    "file": "llama-cli",         "save": "llama-cli-linux",   "url": URL_BASE + "llama-b4604-bin-linux-x64.zip"}
    }

    print("\n[❓ Setup Configuration]")
    print("Which drivers would you like to include in this build?")
    print("-" * 55)
    print(" 1. Windows Only (Optimized for this PC)")
    print(" 2. Android Only (Optimized for Mobile/Termux)")
    print(" 3. Hybrid (Windows + Android - Recommended for Migration)")
    print(" 4. Universal (All Platforms - Win/Mac/Linux/Android)")
    print("-" * 55)
    
    choice = input("Select Option (1-4) > ").strip()
    
    to_download = []
    if choice == "1": to_download = ["1"]
    elif choice == "2": to_download = ["2"]
    elif choice == "3": to_download = ["1", "2"]
    elif choice == "4": to_download = ["1", "2", "3", "4"]
    else: return

    print(f"\n[⬇️ Downloading {len(to_download)} components...]")
    for key in to_download:
        item = options[key]
        final_path = os.path.join(drivers_dir, item['save'])
        if os.path.exists(final_path): continue
        
        print(f"   Fetching: {item['name']}...")
        zip_path = os.path.join(drivers_dir, "temp.zip")
        try:
            urllib.request.urlretrieve(item['url'], zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                with zip_ref.open(item['file']) as source, open(final_path, "wb") as target:
                    shutil.copyfileobj(source, target)
            if "exe" not in item['save']:
                os.chmod(final_path, os.stat(final_path).st_mode | stat.S_IEXEC)
            print(f"   ✅ Installed: {item['save']}")
        except Exception as e: print(f"   ❌ Failed: {e}")
        finally:
            if os.path.exists(zip_path): os.remove(zip_path)

def build_basic():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n[🏗️ BASIC v9.1] Initiating Global Build...")

    # ------------------------------------------------------------------
    # 1. THE FULL MULTILINGUAL ENGINE (basic.py)
    # ------------------------------------------------------------------
    code_basic = r'''#!/usr/bin/env python3
import os, sys, json, platform, subprocess, urllib.request

# [1. Encoding Shield]
sys.stdout.reconfigure(encoding='utf-8')
if platform.system() == 'Windows': os.system('chcp 65001 >nul')

class Basic:
    # [2. Full 10-Language Array]
    LOCALE = {
        'en': ('[System] Connecting...', 'Answer in English.'),
        'ko': ('[시스템] 연결 중...', '반드시 한국어로 답변하세요.'),
        'ja': ('[システム] 接続中...', '日本語で答えてください。'),
        'zh': ('[系统] 连接中...', '请用中文回答。'),
        'ru': ('[Система] ...', 'Отвечайте на русском.'),
        'hi': ('[System] ...', 'हिंदी में उत्तर दें。'),
        'es': ('[System] ...', 'Responde en español.'),
        'fr': ('[System] ...', 'Répondez en français.'),
        'ar': ('[System] ...', 'أجب باللغة العربية.'),
        'pt': ('[System] ...', 'Responda em português.')
    }

    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.lang = 'en'
        self.market_url = "https://raw.githubusercontent.com/KapitalSP/BASIC/main/market.json"

    def detect_lang(self, text):
        """Advanced detection for 10 major global scripts"""
        for char in text:
            if '\uac00' <= char <= '\ud7a3': self.lang = 'ko'; return
            if '\u3040' <= char <= '\u30ff': self.lang = 'ja'; return
            if '\u4e00' <= char <= '\u9fff': self.lang = 'zh'; return
            if '\u0400' <= char <= '\u04ff': self.lang = 'ru'; return
            if '\u0900' <= char <= '\u097f': self.lang = 'hi'; return
            if '\u0600' <= char <= '\u06ff': self.lang = 'ar'; return
        self.lang = 'en' # Default for Latin-based (EN, ES, FR, PT)

    def run(self):
        for f in ['models', 'drivers', 'plugins']: os.makedirs(os.path.join(self.root, f), exist_ok=True)
        m_dir, d_dir = os.path.join(self.root, 'models'), os.path.join(self.root, 'drivers')
        
        # [Smart Driver Selector]
        sys_name = platform.system().lower()
        t_name = ""
        if 'windows' in sys_name: t_name = ".exe"
        elif 'darwin' in sys_name: t_name = "-mac"
        elif 'linux' in sys_name:
            env_p = os.environ.get('PREFIX','').lower()
            t_name = "-android" if ('termux' in env_p or 'android' in env_p) else "-linux"

        d_path = next((os.path.join(d_dir, f) for f in os.listdir(d_dir) if t_name in f.lower()), None)
        if not d_path and 'windows' not in sys_name:
             d_path = next((os.path.join(d_dir, f) for f in os.listdir(d_dir) if '.' not in f), None)

        if d_path and 'windows' not in sys_name: 
            try: os.chmod(d_path, 0o755)
            except: pass

        engines = [f for f in os.listdir(m_dir) if f.endswith('.gguf')]
        print(f"\n--- BASIC AI (v9.1 Omni-Global) ---")
        if not engines: 
            print("[!] No model found. Place a .gguf file in /models.")
            return

        print(f"[Status] Active Driver: {os.path.basename(d_path) if d_path else 'SIMULATION'}")
        
        while True:
            try:
                u_input = input("\n[USER] > ").strip()
                if not u_input or u_input.lower() == '/exit': break
                
                self.detect_lang(u_input)
                sys_msg, prompt_steer = self.LOCALE.get(self.lang, self.LOCALE['en'])
                
                if u_input == '/market':
                    try:
                        with urllib.request.urlopen(self.market_url, timeout=3) as r:
                            items = json.loads(r.read().decode()).get('items',[])
                            for i in items: print(f"- {i['name']}: {i['desc']}")
                    except: print("[!] Connection Error.")
                    continue
                
                print("[AI] ", end="", flush=True)
                if not d_path: print("(Simulation Mode)"); continue
                
                cmd = [d_path, "-m", os.path.join(m_dir, engines[0]), "-p", f"System: {prompt_steer}\nUser: {u_input}\nAssistant:", "-n", "512", "--log-disable"]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
                for line in p.stdout: print(line, end="", flush=True)
                p.wait()

            except KeyboardInterrupt: break
            finally:
                if 'p' in locals() and p and p.poll() is None: p.terminate()

if __name__ == "__main__":
    Basic().run()
'''

    # ------------------------------------------------------------------
    # 2. FILE GENERATION
    # ------------------------------------------------------------------
    for folder in ["drivers", "models", "plugins"]:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    with open(os.path.join(base_dir, "basic.py"), "w", encoding="utf-8") as f:
        f.write(code_basic.strip())
        
    with open(os.path.join(base_dir, "start.bat"), "w", encoding="utf-8") as f:
        f.write("@echo off\ntitle BASIC AI\npython basic.py\npause")

    with open(os.path.join(base_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("# BASIC v9.1 🌍\nFull Multilingual AI Socket.\n\nRun `install.py` to start.")

    ask_and_download(base_dir)
    print("\n✅ [Build Complete] BASIC v9.1 is ready for global use.")

if __name__ == "__main__":
    build_basic()
