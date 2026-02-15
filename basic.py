# Copyright 2026 KapitalSP
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# http://www.apache.org/licenses/LICENSE-2.0

import os, sys, platform, json, subprocess, time, urllib.request, zipfile, shutil, stat

# ==============================================================================
# 🛡️ KAPITAL SENTINEL [UNIVERSAL CORE MANAGER]
# ==============================================================================
try: 
    import psutil
    HAS_DEPS = True
except ImportError: 
    HAS_DEPS = False

class KapitalSentinel:
    def __init__(self, role="worker"):
        self.os = platform.system()
        self.ignite(role)

    def ignite(self, role):
        if not HAS_DEPS: return
        try:
            p = psutil.Process(os.getpid())
            # 1. Priority Boost
            if self.os == "Windows": p.nice(psutil.HIGH_PRIORITY_CLASS)
            else: 
                try: p.nice(-10)
                except: pass
            
            # 2. Smart Core Affinity (OS Breathing Room)
            cores = psutil.cpu_count(logical=True)
            if role == "worker" and cores:
                reserve = 1 if cores > 2 else 0
                if cores > 4: reserve = 2
                try: p.cpu_affinity(list(range(cores - reserve)))
                except: pass
            print(f" [🛡️] SENTINEL ACTIVE: {role.upper()} Mode")
        except: pass

# Start Sentinel immediately
sentinel = KapitalSentinel("worker")

# ==============================================================================
# 🏭 BASIC CHASSIS v3.1 [GLOBAL]
# ==============================================================================
ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT, "config.json")

class SystemUtils:
    @staticmethod
    def get_binary_name():
        return "llama-cli.exe" if platform.system() == "Windows" else "llama-cli"
    
    @staticmethod
    def get_driver_path():
        return os.path.join(ROOT, 'drivers', SystemUtils.get_binary_name())
    
    @staticmethod
    def recover_engine():
        print("\n [SYSTEM] Engine missing. Initiating Auto-Recovery...")
        sys_os = platform.system().lower()
        URL_BASE = "https://github.com/ggerganov/llama.cpp/releases/download/b4604/"
        target = URL_BASE + ("llama-b4604-bin-win-avx-x64.zip" if 'win' in sys_os else "llama-b4604-bin-linux-x64.zip")
        if 'darwin' in sys_os: target = URL_BASE + "llama-b4604-bin-macos-arm64.zip"

        d_dir = os.path.join(ROOT, 'drivers')
        os.makedirs(d_dir, exist_ok=True)
        zip_path = os.path.join(d_dir, "temp_engine.zip")
        
        try:
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            print(f" [i] Fetching from: {target}")
            urllib.request.urlretrieve(target, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as z:
                for n in z.namelist():
                    if 'llama-cli' in n and not n.endswith('/'):
                        with z.open(n) as s, open(SystemUtils.get_driver_path(), "wb") as t:
                            shutil.copyfileobj(s, t)
            
            if 'win' not in sys_os:
                st = os.stat(SystemUtils.get_driver_path())
                os.chmod(SystemUtils.get_driver_path(), st.st_mode | stat.S_IEXEC)
            print(" [OK] Engine binary restored.")
            return True
        except Exception as e:
            print(f" [ERR] Recovery Failed: {e}")
            return False
        finally:
            if os.path.exists(zip_path): os.remove(zip_path)

class Engine:
    def run(self):
        driver = SystemUtils.get_driver_path()
        if not os.path.exists(driver): 
            if not SystemUtils.recover_engine(): return
        
        mdir = os.path.join(ROOT, 'models')
        os.makedirs(mdir, exist_ok=True)
        models = [f for f in os.listdir(mdir) if f.endswith('.gguf')]
        
        if not models:
            print(f" [!] Error: No models found. Please place a .gguf file in: {mdir}")
            input(" Press Enter to return...")
            return

        model_path = os.path.abspath(os.path.join(mdir, models[0]))
        print(f" [🚀] IGNITION: {models[0]}")
        
        cmd = [driver, "-m", model_path, "-p", "User: Hello\nAI:", "-cnv", "--log-disable"]
        try: subprocess.run(cmd)
        except KeyboardInterrupt: pass

if __name__ == "__main__":
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(" ==========================================")
        print(" 🏭 BASIC v3.1 // STANDALONE RUNNER")
        print(" ==========================================")
        print(" [S] START ENGINE")
        print(" [Q] QUIT")
        
        cmd = input("\n Command > ").lower().strip()
        if cmd == 'q': break
        elif cmd == 's': Engine().run()
