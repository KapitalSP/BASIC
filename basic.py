import os
import multiprocessing
import platform

class Basic:
    """
    BASIC v1.0: The Fundamental Infrastructure for Local AI.
    A minimalist, pure Python skeleton for permanent engine sockets.
    """
    def __init__(self):
        self.version = "1.0.0"
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.slots = ["models", "refinery", "logs", "plugins"]

    def initialize(self):
        print(f"--- [BASIC v{self.version}] Framework Initializing ---")
        
        # 1. Build Physical Slots (Folders)
        for slot in self.slots:
            path = os.path.join(self.root, slot)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"[OK] Slot Created: /{slot}")

        # 2. Hardware Resource Scan
        cpu_cores = multiprocessing.cpu_count()
        print(f"[ENV] Logic Cores: {cpu_cores}")
        print(f"[ENV] OS: {platform.system()} ({platform.machine()})")

        # 3. Universal Socket Connection
        model_dir = os.path.join(self.root, "models")
        engine_files = [f for f in os.listdir(model_dir) if f.endswith(".gguf")]
        
        if not engine_files:
            print("\n[ALERT] No engine detected.")
            print(">> Action Required: Place a .gguf engine file in /models.")
            return

        self.active_engine = engine_files[0]
        print(f"[SOCKET] Mounted Engine: {self.active_engine}")
        self.start_session()

    def start_session(self):
        print("\n--- BASIC Eternal Session Active ---")
        print("Offline mode. Zero-token. Permanent ownership.")
        
        while True:
            try:
                user_input = input("\n[USER] > ").strip()
                if not user_input: continue
                if user_input.lower() in ['exit', 'quit']: break
                
                # INTERFACE: Placeholder for the inference engine bridge
                print(f"[BASIC] Bridge: Forwarding input to '{self.active_engine}'...")
                print(f"[INFO] Running on internal resources. Awaiting modded inference logic.")
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    Basic().initialize()
