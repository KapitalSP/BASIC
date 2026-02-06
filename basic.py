#!/usr/bin/env python3
import os
import multiprocessing
import platform
import subprocess
import sys

class Basic:
    """
    BASIC v1.2: The Universal Socket.
    Powered by Native Subprocess Bridge. No Dependencies.
    """
    def __init__(self):
        self.version = "1.2.0"
        self.root = os.path.dirname(os.path.abspath(__file__))
        # Core slots for the infrastructure
        self.slots = ["models", "drivers", "refinery", "logs", "plugins"]
        self.active_engine = None
        self.active_driver = None

    def initialize(self):
        print(f"--- [BASIC v{self.version}] Framework Initializing ---")
        
        # 1. Build Physical Slots (Create folders if not exist)
        for slot in self.slots:
            path = os.path.join(self.root, slot)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"[OK] Slot Created: /{slot}")

        # 2. Resource & Socket Scan
        self.check_resources()
        
        # 3. Mount Components and Start
        if self.mount_components():
            self.start_session()

    def check_resources(self):
        # Display hardware and OS info for debugging
        print(f"[ENV] Logic Cores: {multiprocessing.cpu_count()}")
        print(f"[ENV] OS: {platform.system()} ({platform.machine()})")

    def mount_components(self):
        # Scan for Engine Files (.gguf)
        model_dir = os.path.join(self.root, "models")
        # Sort files alphabetically for consistent loading
        engines = sorted([
            f for f in os.listdir(model_dir) 
            if f.endswith(".gguf") and os.path.isfile(os.path.join(model_dir, f))
        ])
        
        # Scan for Driver Files (Executables)
        driver_dir = os.path.join(self.root, "drivers")
        drivers = sorted([
            f for f in os.listdir(driver_dir) 
            if not f.startswith(".") and os.path.isfile(os.path.join(driver_dir, f))
        ])

        # Critical Check: Engine is mandatory
        if not engines:
            print("\n[ALERT] No engine (.gguf) found in /models.")
            print(">> Action Required: Place a .gguf file in the /models directory.")
            return False
        
        # Driver Check: Optional (Falls back to simulation mode)
        if not drivers:
            print("\n[INFO] No driver found in /drivers. Running in Placeholder Mode.")
            self.active_driver = None
        else:
            self.active_driver = os.path.join(driver_dir, drivers[0])
            
            # [Auto-Patch] Grant execution permissions for Linux/macOS
            if platform.system() != "Windows":
                try:
                    os.chmod(self.active_driver, 0o755)
                    print(f"[SEC] Permission Granted: +x to {drivers[0]}")
                except Exception as e:
                    print(f"[WARN] Failed to set permissions: {e}")

            print(f"[SOCKET] Driver Mounted: {drivers[0]}")

        self.active_engine = os.path.join(model_dir, engines[0])
        print(f"[SOCKET] Engine Mounted: {engines[0]}")
        return True

    def start_session(self):
        print("\n--- BASIC Eternal Session Active ---")
        print("Type 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("\n[USER] > ").strip()
                if not user_input: continue
                if user_input.lower() in ['exit', 'quit']: break
                
                if self.active_driver:
                    self.run_subprocess(user_input)
                else:
                    # Placeholder Mode (When no driver is installed)
                    print(f"[BASIC] Bridge: Forwarding to {os.path.basename(self.active_engine)}...")
                    print("[INFO] Install a driver (e.g., llama-cli) in /drivers to activate real inference.")

            except KeyboardInterrupt:
                print("\n[System] Interrupted.")
                break
            except EOFError: # Handle Ctrl+D gracefully
                break

    def run_subprocess(self, prompt):
        print("[AI] ", end="", flush=True)
        
        # Construct the command for the driver
        command = [
            self.active_driver,
            "-m", self.active_engine,
            "-p", prompt,
            "-n", "512",       # Token limit
            "--log-disable"    # Suppress system logs
        ]

        process = None
        try:
            # Execute the driver using native subprocess
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                encoding='utf-8',   # Force UTF-8
                errors='replace'    # Prevent crashing on encoding errors
            )
            
            # Stream the output in real-time
            for line in process.stdout:
                print(line, end="", flush=True)
            
            # Check for errors after execution
            _, stderr = process.communicate()
            if stderr and process.returncode != 0:
                print(f"\n[Engine Error] {stderr}")
            
        except Exception as e:
            print(f"\n[ERROR] Bridge Failure: {e}")
            print(">> Check if the driver is compatible with your OS.")
            
        finally:
            # [Safety] Kill zombie processes if the loop breaks
            if process and process.poll() is None:
                process.terminate()
                process.wait()

if __name__ == "__main__":
    Basic().initialize()

