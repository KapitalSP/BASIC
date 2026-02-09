import os, sys, platform, urllib.request, zipfile, shutil, stat, json

# ==============================================================================
# 🏗️ BASIC INSTALLER (The Foundation Builder)
# ==============================================================================

ROOT = os.path.dirname(os.path.abspath(__file__))
DIRS = ['models', 'drivers', 'plugins']

def log(msg): print(f" [INSTALL] {msg}")

def create_default_market():
    market_path = os.path.join(ROOT, "market.json")
    if not os.path.exists(market_path):
        default_data = {
            "version": "1.0",
            "motd": "Welcome to BASIC Tera-Scale Platform",
            "items": [
                {"name": "Deep-Thinker 100B", "type": "Model", "desc": "Reasoning optimized model."},
                {"name": "Auto-Cleaner", "type": "Plugin", "desc": "RAM garbage collector script."},
                {"name": "Cluster-Link", "type": "Driver", "desc": "Multi-node connection tool."}
            ]
        }
        with open(market_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        log("Marketplace registry initialized.")
    else:
        log("Marketplace registry exists. Skipping.")

def setup_environment():
    log("Initializing Trust Grid structure...")
    
    # 1. Create Grid Layout
    for d in DIRS:
        path = os.path.join(ROOT, d)
        os.makedirs(path, exist_ok=True)

    # 2. Initialize Market
    create_default_market()

    # 3. Detect OS & Select Driver
    sys_os = platform.system().lower()
    URL_BASE = "https://github.com/ggerganov/llama.cpp/releases/download/b4604/"
    
    if 'windows' in sys_os:
        target_url = URL_BASE + "llama-b4604-bin-win-avx-x64.zip"
        bin_name = "llama-cli.exe"
    elif 'darwin' in sys_os:
        target_url = URL_BASE + "llama-b4604-bin-macos-arm64.zip"
        bin_name = "llama-cli-mac"
    else:
        target_url = URL_BASE + "llama-b4604-bin-linux-x64.zip"
        bin_name = "llama-cli-linux"

    driver_path = os.path.join(ROOT, 'drivers', bin_name)

    # 4. Download & Install Driver
    if not os.path.exists(driver_path):
        log(f"Downloading Core Engine for {sys_os.upper()}...")
        try:
            zip_path = os.path.join(ROOT, 'drivers', "temp_core.zip")
            urllib.request.urlretrieve(target_url, zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as z:
                for n in z.namelist():
                    if 'llama-cli' in n:
                        with z.open(n) as s, open(driver_path, "wb") as t:
                            shutil.copyfileobj(s, t)
            
            if 'windows' not in sys_os:
                st = os.stat(driver_path)
                os.chmod(driver_path, st.st_mode | stat.S_IEXEC)
                
            log("Engine installed successfully.")
        except Exception as e:
            log(f"CRITICAL ERROR: {e}")
        finally:
            if os.path.exists(zip_path): os.remove(zip_path)
    else:
        log("Engine already exists. Skipping.")

    log("Construction Complete.")

if __name__ == "__main__":
    setup_environment()
