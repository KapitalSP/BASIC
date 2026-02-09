import os, sys, subprocess, platform, threading, queue, time

# ==============================================================================
# 🎛️ BASIC v4.0 [HYPER-TUNER]
# Feature: Auto-Tuning Dashboard (CPU/GPU Controller)
# ==============================================================================

# [Default Config]
CONFIG = {
    "threads": os.cpu_count() or 4,
    "gpu_layers": 999,      # Max Offload
    "ctx_size": 4096,       # Context Memory
    "flash_attn": True      # Speed Boost
}

IS_MOBILE = 'termux' in str(os.environ) or 'android' in str(os.environ)

class Tuner:
    def __init__(self):
        self.clear_screen()
        self.dashboard()

    def clear_screen(self):
        os.system("clear" if IS_MOBILE or os.name!='nt' else "cls")

    def dashboard(self):
        while True:
            self.clear_screen()
            print(" ┌──────────────────────────────────────────┐")
            print(f" │ 🎛️  HYPER-TUNER // SYSTEM CONTROL       │")
            print(" ├──────────────────────────────────────────┤")
            print(f" │ [1] CPU Threads  : {CONFIG['threads']} (Cores)")
            print(f" │ [2] GPU Layers   : {CONFIG['gpu_layers']} (Offload)")
            print(f" │ [3] Context Size : {CONFIG['ctx_size']} (Tokens)")
            print(f" │ [4] Flash Attn   : {'ON' if CONFIG['flash_attn'] else 'OFF'} (Speed)")
            print(" ├──────────────────────────────────────────┤")
            print(" │ [A] Auto-Optimize (Detect Hardware)      │")
            print(" │ [S] START ENGINE (Apply & Run)           │")
            print(" └──────────────────────────────────────────┘")
            
            cmd = input(" 🔧 Select > ").lower().strip()
            
            if cmd == 's' or cmd == '': break
            elif cmd == 'a': self.auto_tune()
            elif cmd == '1': self.set_val("threads")
            elif cmd == '2': self.set_val("gpu_layers")
            elif cmd == '3': self.set_val("ctx_size")
            elif cmd == '4': CONFIG['flash_attn'] = not CONFIG['flash_attn']

    def set_val(self, key):
        try:
            val = input(f" Set {key} value: ")
            if val.isdigit(): CONFIG[key] = int(val)
        except: pass

    def auto_tune(self):
        print(" [!] Scanning Hardware...")
        time.sleep(0.5)
        if IS_MOBILE:
            # Mobile: Balance (Heat Management)
            CONFIG['threads'] = max(2, (os.cpu_count() or 4) - 2)
            CONFIG['ctx_size'] = 2048
            CONFIG['flash_attn'] = False # Stability
        else:
            # PC: Performance (Max Power)
            CONFIG['threads'] = os.cpu_count() or 8
            CONFIG['ctx_size'] = 8192
            CONFIG['flash_attn'] = True
        print(" [!] Optimization Complete.")
        time.sleep(0.5)

class Engine:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.driver, self.model = self._scan()
        self.q = queue.Queue()
        self.proc = None

    def _scan(self):
        # Driver
        if IS_MOBILE: drv = "llama-cli"
        else:
            sys_os = platform.system()
            b = "llama-cli.exe" if sys_os=='Windows' else "llama-cli-mac" if sys_os=='Darwin' else "llama-cli-linux"
            drv = os.path.join(self.root, 'drivers', b)

        # Model
        mdir = os.path.join(os.environ.get('HOME','.'), 'models') if IS_MOBILE else os.path.join(self.root, 'models')
        try: m = os.path.join(mdir, [f for f in os.listdir(mdir) if f.endswith('.gguf')][0])
        except: m = None
        return drv, m

    def _reader(self, stream):
        for line in iter(stream.readline, ''): self.q.put(line)
        stream.close()

    def run(self):
        if not self.model: return print(" [!] Error: No model file found.")
        
        # Build Command based on Tuner Config
        flags = [
            "-t", str(CONFIG['threads']),
            "-ngl", str(CONFIG['gpu_layers']),
            "-c", str(CONFIG['ctx_size']),
            "-b", "512", "--log-disable"
        ]
        if CONFIG['flash_attn']: flags.append("-fa")

        print(f"\n [🚀] Engine Ignition... (Threads: {CONFIG['threads']} | GPU: {CONFIG['gpu_layers']})")
        
        while True:
            try:
                p = input("\n You: ").strip()
                if not p: continue
                if p.lower() in ['exit', 'quit']: break

                cmd = [self.driver, "-m", self.model, "-p", f"User: {p}\nAssistant:"] + flags
                
                self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8', errors='replace', bufsize=1)
                t = threading.Thread(target=self._reader, args=(self.proc.stdout,), daemon=True)
                t.start()

                print(" AI: ", end="", flush=True)
                while self.proc.poll() is None or not self.q.empty():
                    try:
                        line = self.q.get(timeout=0.01)
                        print(line, end="", flush=True)
                    except queue.Empty: continue
                
            except KeyboardInterrupt: break

if __name__ == "__main__":
    try:
        Tuner() # Show Dashboard First
        Engine().run() # Start Engine
    except KeyboardInterrupt: pass
