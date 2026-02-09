import os, sys, subprocess, platform, json

# ==============================================================================
# 💎 BASIC ENGINE v10.2 (Tera-Scale + Market)
# Optimized for 1,000B+ Distributed Inference with Marketplace Integration
# ==============================================================================

class BasicCore:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.driver_dir = os.path.join(self.root, 'drivers')
        self.model_dir = os.path.join(self.root, 'models')
        self.plugin_dir = os.path.join(self.root, 'plugins')
        self.market_file = os.path.join(self.root, 'market.json')

    def load_plugins(self):
        # [Extension Slot]
        if not os.path.exists(self.plugin_dir): return
        plugins = [f for f in os.listdir(self.plugin_dir) if f.endswith('.py')]
        if not plugins: return

        print(f"[BASIC] Found {len(plugins)} plugins. Engaging...")
        for plugin in plugins:
            try:
                path = os.path.join(self.plugin_dir, plugin)
                with open(path, 'r', encoding='utf-8') as f:
                    exec(f.read(), globals())
                print(f"   + Loaded: {plugin}")
            except Exception as e:
                print(f"   ! Failed: {plugin} ({e})")
        print("")

    def show_market(self):
        # [Marketplace Viewer]
        if not os.path.exists(self.market_file):
            print("[BASIC] Market registry not found. Run install.py first.")
            return

        try:
            with open(self.market_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n--- 🛒 BASIC Market v{data.get('version', '1.0')} ---")
            print(f"MOTD: {data.get('motd', 'No message')}")
            print("-" * 40)
            print(f"{'TYPE':<10} | {'NAME':<20} | {'DESC'}")
            print("-" * 40)
            for item in data.get('items', []):
                print(f"{item.get('type','Item'):<10} | {item.get('name','Unknown'):<20} | {item.get('desc','')}")
            print("-" * 40 + "\n")
        except Exception as e:
            print(f"[BASIC] Market Error: {e}")

    def ignite(self):
        # 0. Load Plugins
        self.load_plugins()

        # 1. Blind Bind
        sys_os = platform.system()
        bin_name = "llama-cli.exe" if sys_os == 'Windows' else "llama-cli"
        if sys_os != 'Windows':
            if 'darwin' in sys_os.lower(): bin_name = "llama-cli-mac"
            else: bin_name = "llama-cli-linux"

        driver_path = os.path.join(self.driver_dir, bin_name)
        
        # 2. Auto-Select Model
        try:
            model_file = [f for f in os.listdir(self.model_dir) if f.endswith('.gguf')][0]
            model_path = os.path.join(self.model_dir, model_file)
        except (IndexError, FileNotFoundError):
            print("[BASIC] Error: No GGUF model found in /models", file=sys.stderr)
            return

        print(f"[BASIC] Tera-Link Established: {model_file}")
        print(f"        (Mode: Distributed / Zero-Latency Pipe)\n")
        print("        (Type '/market' to browse extensions)\n")

        # 3. Main Protocol Loop
        while True:
            try:
                prompt = input().strip()
                if not prompt: continue
                
                # [Command Hook]
                if prompt == '/exit': break
                if prompt == '/market': 
                    self.show_market()
                    continue # Do not send to AI

                # [Tera-Scale Optimization]
                cmd = [
                    driver_path, 
                    "-m", model_path, 
                    "-p", f"User: {prompt}\nAI:", 
                    "-n", "512", 
                    "--log-disable",
                    "-ngl", "999", "-sm", "row"
                ]
                
                if sys_os == 'Linux': cmd.extend(["--numa", "dist"])

                p_args = {"bufsize": 0}
                if sys_os != 'Windows': p_args["pass_fds"] = (sys.stdout.fileno(),)

                p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, **p_args)
                p.wait()
                print("") 

            except KeyboardInterrupt: break
            except EOFError: break

if __name__ == "__main__":
    BasicCore().ignite()
