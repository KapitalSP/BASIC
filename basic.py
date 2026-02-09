import os, sys, subprocess, platform

# ==============================================================================
# 💎 BASIC ENGINE v10.1 (Tera-Scale + Plugin Slot)
# Optimized for 1,000B+ Distributed Inference with Minimal Extensibility
# ==============================================================================

class BasicCore:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.driver_dir = os.path.join(self.root, 'drivers')
        self.model_dir = os.path.join(self.root, 'models')
        self.plugin_dir = os.path.join(self.root, 'plugins')

    def load_plugins(self):
        # [Extension Slot]
        # Executes .py files in /plugins before the engine starts.
        if not os.path.exists(self.plugin_dir): return
        
        plugins = [f for f in os.listdir(self.plugin_dir) if f.endswith('.py')]
        if not plugins: return

        print(f"[BASIC] Found {len(plugins)} plugins. Engaging...")
        for plugin in plugins:
            try:
                path = os.path.join(self.plugin_dir, plugin)
                # Raw Execution for maximum trust & speed
                with open(path, 'r', encoding='utf-8') as f:
                    exec(f.read(), globals())
                print(f"   + Loaded: {plugin}")
            except Exception as e:
                print(f"   ! Failed: {plugin} ({e})")
        print("")

    def ignite(self):
        # 0. Load Plugins (The B-Side)
        self.load_plugins()

        # 1. Blind Bind (Trust Mode)
        sys_os = platform.system()
        bin_name = "llama-cli.exe" if sys_os == 'Windows' else "llama-cli"
        if sys_os != 'Windows':
            if 'darwin' in sys_os.lower(): bin_name = "llama-cli-mac"
            else: bin_name = "llama-cli-linux"

        driver_path = os.path.join(self.driver_dir, bin_name)
        
        # 2. Auto-Select First Model
        try:
            model_file = [f for f in os.listdir(self.model_dir) if f.endswith('.gguf')][0]
            model_path = os.path.join(self.model_dir, model_file)
        except (IndexError, FileNotFoundError):
            print("[BASIC] Error: No GGUF model found in /models", file=sys.stderr)
            return

        print(f"[BASIC] Tera-Link Established: {model_file}")
        print(f"        (Mode: Distributed / Zero-Latency Pipe)\n")

        # 3. Main Protocol Loop
        while True:
            try:
                prompt = input().strip()
                if not prompt: continue
                if prompt == '/exit': break
                
                # [Tera-Scale Optimization]
                # 1. -sm row : Split Mode Row (Essential for Multi-GPU)
                # 2. -ngl 999 : GPU Offload Max (Full VRAM Usage)
                
                cmd = [
                    driver_path, 
                    "-m", model_path, 
                    "-p", f"User: {prompt}\nAI:", 
                    "-n", "512", 
                    "--log-disable",
                    "-ngl", "999",      # GPU Full Offload
                    "-sm", "row"        # Multi-GPU Split Strategy
                ]
                
                # NUMA awareness for Linux servers (1TB RAM handling)
                if sys_os == 'Linux':
                    cmd.extend(["--numa", "dist"])

                # Direct Pipe Optimization (No Buffering)
                p_args = {"bufsize": 0}
                if sys_os != 'Windows': p_args["pass_fds"] = (sys.stdout.fileno(),)

                p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, **p_args)
                p.wait()
                print("") 

            except KeyboardInterrupt:
                break
            except EOFError:
                break

if __name__ == "__main__":
    BasicCore().ignite()
