import os
import sys
import json
import platform
import urllib.request
import zipfile
import shutil
import stat

# ==============================================================================
# 🏭 BASIC v9.2 (Final Release Edition)
# The Omni-Platform Self-Generating AI Ecosystem.
# No dependencies. No manual setup. Just Intelligence.
# ==============================================================================

def build_ecosystem():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n[🏗️ BASIC v9.2] Initializing Factory in: {base_dir}")

    # ------------------------------------------------------------------
    # 1. GENERATE THE ENGINE (basic.py)
    # ------------------------------------------------------------------
    code_basic = r'''#!/usr/bin/env python3
import os, sys, json, platform, subprocess, urllib.request

# [System Shield] Encoding & Buffer setup
sys.stdout.reconfigure(encoding='utf-8')
if platform.system() == 'Windows': os.system('chcp 65001 >nul')

class Basic:
    # [Full 10-Language Nerve System]
    LOCALE = {
        'en': ('[System] Connecting...', 'Answer in English.'),
        'ko': ('[시스템] 접속 중...', '반드시 한국어로 답변하세요.'),
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
        self.market_file = os.path.join(self.root, "market.json")

    def detect_lang(self, text):
        for char in text:
            if '\uac00' <= char <= '\ud7a3': self.lang = 'ko'; return
            if '\u3040' <= char <= '\u30ff': self.lang = 'ja'; return
            if '\u4e00' <= char <= '\u9fff': self.lang = 'zh'; return
            if '\u0400' <= char <= '\u04ff': self.lang = 'ru'; return
            if '\u0900' <= char <= '\u097f': self.lang = 'hi'; return
            if '\u0600' <= char <= '\u06ff': self.lang = 'ar'; return
        self.lang = 'en'

    def run(self):
        # Create Slots
        for f in ['models', 'drivers', 'plugins', 'logs']:
            os.makedirs(os.path.join(self.root, f), exist_ok=True)
            
        m_dir, d_dir = os.path.join(self.root, 'models'), os.path.join(self.root, 'drivers')
        
        # [Omni-Selector: PC & Android Awareness]
        sys_name = platform.system().lower()
        t_name = ".exe" if 'windows' in sys_name else "-mac" if 'darwin' in sys_name else \
                 "-android" if ('termux' in os.environ.get('PREFIX','') or 'android' in os.environ.get('PREFIX','')) else "-linux"

        d_path = next((os.path.join(d_dir, f) for f in os.listdir(d_dir) if t_name in f.lower()), None)
        if not d_path and 'windows' not in sys_name:
             d_path = next((os.path.join(d_dir, f) for f in os.listdir(d_dir) if '.' not in f), None)

        if d_path and 'windows' not in sys_name: 
            try: os.chmod(d_path, 0o755)
            except: pass

        engines = [f for f in os.listdir(m_dir) if f.endswith('.gguf')]
        print(f"\n--- BASIC AI (v9.2 Final) ---")
        
        # [Plugin Scan]
        p_files = [f for f in os.listdir(os.path.join(self.root, 'plugins')) if f.endswith('.py')]
        if p_files: print(f"[System] Active Plugins: {len(p_files)} modules loaded.")

        if not engines: 
            print("[!] No model detected. Place a .gguf file in /models.")
            return

        print(f"[System] Driver: {os.path.basename(d_path) if d_path else 'SIMULATION'}\n")
        
        while True:
            try:
                u = input("[USER] > ").strip()
                if not u or u.lower() == '/exit': break
                self.detect_lang(u)
                sys_msg, prompt = self.LOCALE.get(self.lang, self.LOCALE['en'])
                
                if u == '/market':
                    if os.path.exists(self.market_file):
                        with open(self.market_file, "r") as f:
                            data = json.load(f)
                            print(f"--- Marketplace v{data.get('version')} ---")
                            for i in data.get('items', []): print(f"- {i['name']}: {i['desc']}")
                    else: print("[!] Market file not found.")
                    continue
                
                print("[AI] ", end="", flush=True)
                if not d_path: print("(Simulation Mode)"); continue
                
                cmd = [d_path, "-m", os.path.join(m_dir, engines[0]), "-p", f"System: {prompt}\nUser: {u}\nAssistant:", "-n", "512", "--log-disable"]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
                for line in p.stdout: print(line, end="", flush=True)
                p.wait()
            except KeyboardInterrupt: break
            finally:
                if 'p' in locals() and p and p.poll() is None: p.terminate()

if __name__ == "__main__": Basic().run()
'''

    # ------------------------------------------------------------------
    # 2. FILE GENERATION (Self-Creation Logic)
    # ------------------------------------------------------------------
    # [2-1] market.json (Self-Generation)
    market_data = {
        "version": "1.0",
        "items": [
            {"name": "Real-time Search", "desc": "Live web access module."},
            {"name": "Voice Core", "desc": "Local TTS/STT engine."}
        ]
    }
    
    # [2-2] Create Project Files
    files = {
        "basic.py": code_basic.strip(),
        "market.json": json.dumps(market_data, indent=4),
        "start.bat": "@echo off\ntitle BASIC\npython basic.py\npause",
        "README.md": "# BASIC v9.2\nKnowledge Sovereignty.\n\n1. Run `install.py`\n2. Add `.gguf` to `/models`"
    }

    for name, content in files.items():
        with open(os.path.join(base_dir, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   [+] Generated: {name}")

    # ------------------------------------------------------------------
    # 3. INTERACTIVE DRIVER DOWNLOAD
    # ------------------------------------------------------------------
    drivers_dir = os.path.join(base_dir, "drivers")
    os.makedirs(drivers_dir, exist_ok=True)
    URL_BASE = "https://github.com/ggerganov/llama.cpp/releases/download/b4604/"
    
    options = {
        "1": {"name": "Windows (PC)", "f": "llama-cli.exe", "s": "llama-cli.exe", "u": URL_BASE + "llama-b4604-bin-win-avx-x64.zip"},
        "2": {"name": "Android (Phone)", "f": "llama-cli", "s": "llama-cli-android", "u": URL_BASE + "llama-b4604-bin-android-arm

