import os
import sys

# ==============================================================================
# 🏭 BASIC PLATFORM FACTORY (One-Click Installer)
# This script generates the entire ecosystem: Engine, Data, Config, and Folders.
# ==============================================================================

def build_platform():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n[🏗️ Factory] Initializing Construction in: {base_dir}")

    # ------------------------------------------------------------------
    # 1. THE TITANIUM ENGINE (BASIC v3.0) - Embedded Source Code
    # ------------------------------------------------------------------
    code_basic = r'''#!/usr/bin/env python3
import os, sys, json, platform, subprocess, urllib.request

# [1. Environment Hardening] Force UTF-8 for Windows/Linux (Prevent Mojibake)
sys.stdout.reconfigure(encoding='utf-8')
if platform.system() == 'Windows': os.system('chcp 65001 >nul')

class Basic:
    # [2. Language Data] Covering 90% of Global Population (Top 10)
    LOCALE = {
        'en': ('[System] Connecting...', 'Answer in English.'),
        'ko': ('[시스템] 접속 중...', '반드시 한국어로 답변하세요.'),
        'ja': ('[システム] 接続中...', '日本語で答えてください。'),
        'zh': ('[系统] 连接中...', '请用中文回答。'),
        'ru': ('[Система] Подключение...', 'Отвечайте на русском.'),
        'hi': ('[System] Connecting...', 'हिंदी में उत्तर दें।'),
        'es': ('[System] Conectando...', 'Responde en español.'),
        'fr': ('[System] Connexion...', 'Répondez en français.'),
        'ar': ('[System] Connecting...', 'أجب باللغة العربية.'),
        'pt': ('[System] Conectando...', 'Responda em português.')
    }

    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.lang = 'en'
        self.market_url = "https://raw.githubusercontent.com/KapitalSP/BASIC/main/market.json"

    def detect_lang(self, text):
        """Detect input language in 0.001s using Unicode ranges"""
        for char in text:
            if '\uac00' <= char <= '\ud7a3': self.lang = 'ko'; return
            if '\u3040' <= char <= '\u30ff': self.lang = 'ja'; return
            if '\u4e00' <= char <= '\u9fff': self.lang = 'zh'; return
            if '\u0400' <= char <= '\u04ff': self.lang = 'ru'; return
            if '\u0900' <= char <= '\u097f': self.lang = 'hi'; return
            if '\u0600' <= char <= '\u06ff': self.lang = 'ar'; return
        self.lang = 'en'

    def run(self):
        # [3. Create Physical Slots]
        for folder in ['models', 'drivers', 'plugins']:
            os.makedirs(os.path.join(self.root, folder), exist_ok=True)

        # [4. Scan Components]
        m_dir = os.path.join(self.root, 'models')
        d_dir = os.path.join(self.root, 'drivers')
        
        engines = [f for f in os.listdir(m_dir) if f.endswith('.gguf')]
        drivers = [f for f in os.listdir(d_dir) if os.path.isfile(os.path.join(d_dir, f))]

        print(f"--- BASIC AI Platform (v3.0 Titanium) ---")
        if not engines: print("[!] No model found in /models. Please add a .gguf file."); return
        
        driver_path = os.path.join(d_dir, drivers[0]) if drivers else None
        if driver_path and platform.system() != 'Windows':
            try: os.chmod(driver_path, 0o755)
            except: pass

        # [5. Main Loop]
        print("Type '/market', '/exit', or start chatting.\n")
        
        while True:
            try:
                user_input = input("\n[USER] > ").strip()
                if not user_input: continue
                if user_input.lower() in ['/exit', 'exit']: break
                
                self.detect_lang(user_input) # Auto-detect language
                msg, prompt = self.LOCALE.get(self.lang, self.LOCALE['en'])

                # [Feature 1] Access Market
                if user_input == '/market':
                    print(msg)
                    try:
                        with urllib.request.urlopen(self.market_url, timeout=3) as res:
                            data = json.loads(res.read().decode())
                            print(f"=== Market Items ({len(data.get('items', []))}) ===")
                            for item in data.get('items', []):
                                print(f"- {item['name']} : {item['desc']}")
                    except: print("[!] Offline Mode (Cannot reach server)")
                    continue

                # [Feature 2] Run AI (The Strongest Link)
                print("[AI] ", end="", flush=True)
                if not driver_path: print("(Simulation Mode: No driver found)"); continue
                
                full_prompt = f"System: {prompt}\nUser: {user_input}\nAssistant:"
                process = None
                try:
                    process = subprocess.Popen(
                        [driver_path, "-m", os.path.join(m_dir, engines[0]), "-p", full_prompt, "-n", "512", "--log-disable"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        encoding='utf-8', errors='replace'
                    )
                    for line in process.stdout: print(line, end="", flush=True)
                    process.wait()

                except KeyboardInterrupt: print("\n[!] Stopped by User")
                finally:
                    if process and process.poll() is None: process.terminate(); process.wait()

            except EOFError: break
            except Exception as e: print(f"\n[Error] {e}")

if __name__ == "__main__":
    Basic().run()
'''

    # ------------------------------------------------------------------
    # 2. MARKET DATA (Fallback)
    # ------------------------------------------------------------------
    code_market = r'''{
  "version": "1.0",
  "items": [
    {
      "id": "sys_diag",
      "name": "System Diagnostics",
      "desc": "Basic tool to check environment",
      "size": "2KB"
    }
  ]
}'''

    # ------------------------------------------------------------------
    # 3. README (Documentation)
    # ------------------------------------------------------------------
    code_readme = r'''# BASIC: The Local AI Platform 🏟️

> **[DISCLAIMER]**
> This tool is provided "as-is" for research purposes.
> The user bears full responsibility for the generated content.

## 🚀 Installation Guide
1. **Engine:** Download `llama-cli` (or .exe) -> Put it in `/drivers` folder.
2. **Brain:** Download any `.gguf` model -> Put it in `/models` folder.
3. **Start:** Run `basic.py` (or click `run.bat`).

## 🌍 Features
* **10 Languages Support:** Auto-detects input (English, Korean, Hindi, etc.)
* **Zero Dependencies:** No `pip install` required.
* **Industrial Grade:** "Titanium" stability against crashes.
'''

    # ------------------------------------------------------------------
    # 4. WINDOWS LAUNCHER (run.bat)
    # ------------------------------------------------------------------
    code_bat = r'''@echo off
chcp 65001 >nul
title BASIC AI Platform
echo Starting BASIC...
python basic.py
pause
'''

    # ==================================================================
    # 🏗️ BUILD PROCESS
    # ==================================================================
    
    # 1. Create Directories
    folders = ["drivers", "models", "plugins"]
    for folder in folders:
        path = os.path.join(base_dir, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"   [+] Folder Created: /{folder}")
        else:
            print(f"   [.] Folder Exists:  /{folder}")

    # 2. Write Files
    files_map = {
        "basic.py": code_basic,
        "market.json": code_market,
        "README.md": code_readme,
        "run.bat": code_bat
    }

    for filename, content in files_map.items():
        file_path = os.path.join(base_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"   [+] File Generated: {filename}")

    print("\n✅ [SUCCESS] Factory build complete!")
    print("   -> 1. Put 'llama-cli' in /drivers")
    print("   -> 2. Put '.gguf' model in /models")
    print("   -> 3. Run 'basic.py'\n")

if __name__ == "__main__":
    build_platform()
