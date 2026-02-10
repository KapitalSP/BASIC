import os, sys, platform, urllib.request, zipfile, shutil, stat, json, time

# ==============================================================================
# 🏗️ BASIC INSTALLER v2.2 (The Foundation Builder)
# Role: Environment Provisioning, Scaffolding, and Engine Retrieval
# ==============================================================================

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION = "2.2.0 (Architect)"

# [1] Directory Structure & Scaffolding Definition
# Defines the folder layout and generates placeholder files for developers.
STRUCTURE = {
    "core": {
        "__init__.py": '"""[CORE]\nEngine logic & Memory management.\n"""',
        "engine.py": '# Core Inference Logic Placeholder\n',
        "memory.py": '# Memory Sharding Logic Placeholder\n'
    },
    "network": {
        "__init__.py": '"""[NETWORK]\nAPI Gateway & Cluster RPC.\n"""',
        "server.py": '# API Server Logic Placeholder\n'
    },
    "utils": {
        "__init__.py": '"""[UTILS]\nSystem Helpers & Logging.\n"""',
        "logger.py": '# Logging Configuration Placeholder\n'
    },
    "drivers": {},  # Binary Storage
    "models": {},   # Model Storage (GGUF)
    "plugins": {},  # Plugin Storage
    "dist": {}      # Build Output Directory
}

# [2] Default Configuration (Compatible with basic.py)
DEFAULT_CONFIG = {
    "system": {
        "role": "BASIC_NODE_MASTER",
        "version": VERSION,
        "debug": True
    },
    "engine": {
        "threads": 4,
        "gpu_layers": 99,
        "ctx_size": 4096,
        "flash_attn": False
    }
}

def log(msg): 
    print(f" [INSTALL] {msg}")

def create_structure_and_config():
    log("Initializing Industrial Scaffolding...")
    
    # 1. Create Folders & Files
    for folder, files in STRUCTURE.items():
        path = os.path.join(ROOT, folder)
        os.makedirs(path, exist_ok=True)
        
        for filename, content in files.items():
            file_path = os.path.join(path, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    # 2. Generate config.json
    if not os.path.exists("config.json"):
        with open("config.json", "w", encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        log("Configuration Schema Generated.")
    else:
        log("Configuration exists. Skipping.")

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

def install_engine():
    sys_os = platform.system().lower()
    URL_BASE = "https://github.com/ggerganov/llama.cpp/releases/download/b4604/"
    
    # OS-specific filename settings (Standardized for basic.py)
    if 'windows' in sys_os:
        target_url = URL_BASE + "llama-b4604-bin-win-avx-x64.zip"
        bin_name = "llama-cli.exe"
    elif 'darwin' in sys_os:
        target_url = URL_BASE + "llama-b4604-bin-macos-arm64.zip"
        bin_name = "llama-cli" 
    else:
        target_url = URL_BASE + "llama-b4604-bin-linux-x64.zip"
        bin_name = "llama-cli"

    driver_path = os.path.join(ROOT, 'drivers', bin_name)

    # 4. Download & Install Driver
    if not os.path.exists(driver_path):
        log(f"Downloading Core Engine for {sys_os.upper()}...")
        try:
            zip_path = os.path.join(ROOT, 'drivers', "temp_core.zip")
            
            # Bypass SSL verification if necessary
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            
            urllib.request.urlretrieve(target_url, zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as z:
                for n in z.namelist():
                    # Robust extraction: flatten structure, ignore internal zip folders
                    if 'llama-cli' in n and not n.endswith('/'):
                        with z.open(n) as s, open(driver_path, "wb") as t:
                            shutil.copyfileobj(s, t)
            
            # Apply execution permissions (Linux/Mac)
            if 'windows' not in sys_os:
                st = os.stat(driver_path)
                os.chmod(driver_path, st.st_mode | stat.S_IEXEC)
                
            log("Engine installed successfully.")
        except Exception as e:
            log(f"CRITICAL ERROR: {e}")
            log("Please manually place 'llama-cli' in /drivers folder.")
        finally:
            if os.path.exists(zip_path): os.remove(zip_path)
    else:
        log("Engine already exists. Skipping.")

if __name__ == "__main__":
    print("="*50)
    print(f" 🏗️  BASIC INSTALLER {VERSION}")
    print("="*50)
    
    try:
        create_structure_and_config() # 1. Create Layout & Config
        create_default_market()       # 2. Initialize Market
        install_engine()              # 3. Fetch Engine
        
        print("\n" + "="*50)
        print(" [SUCCESS] Infrastructure Ready.")
        print("="*50)
        print(" 1. Place .gguf models in '/models'")
        print(" 2. Run 'python basic.py' to launch Control Center")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n [!] Installation Aborted.")
