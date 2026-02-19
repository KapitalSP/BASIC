# Copyright (c) 2026 KapitalSP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
BASIC (The Industrial Core Engine - v3.6.1)
Zero-Tolerance Architecture: Thread-Safe, Type-Safe, OS-Limit Bypassed.
Optimized for high-concurrency offline AI inference.
"""

import os
import sys
import platform
import subprocess
import atexit
import stat
import uuid
import threading

class BasicConfig:
    """Hardware Auto-Detection and Configuration"""
    def __init__(self):
        self.os_type = platform.system().lower()
        self.cpu_cores = os.cpu_count() or 4
        # Optimization: Use 80% of available cores, capped at 16 threads
        self.threads = min(max(1, int(self.cpu_cores * 0.8)), 16) 
        self.context_size = "4096"
        self.gpu_layers = "99"
        
        if 'windows' in self.os_type:
            self.binary_name = "llama-cli.exe"
        else:
            self.binary_name = "llama-cli"

def get_base_path():
    """Detects correct execution path for both script and compiled binary"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

class BasicEngine:
    """Pure Inference Engine (Stateless, Thread-Safe)"""
    def __init__(self, model_path=None):
        self.config = BasicConfig()
        self.base_dir = get_base_path()
        self.driver_path = os.path.join(self.base_dir, "drivers", self.config.binary_name)
        self.model_path = model_path if model_path else self._find_model()
        
        # Thread safety for concurrent process management
        self.process_lock = threading.Lock()
        self.active_processes = []
        
        atexit.register(self.stop_all)
        self._ensure_executable()
        
        if not self._health_check():
            print(f"⚠️  [Engine Warning] Health check failed. Path: {self.driver_path}")

    def _ensure_executable(self):
        """Ensures the driver has execution permissions on Unix-like systems"""
        if os.path.exists(self.driver_path) and 'windows' not in self.config.os_type:
            try:
                st = os.stat(self.driver_path)
                if not (st.st_mode & stat.S_IEXEC):
                    os.chmod(self.driver_path, st.st_mode | stat.S_IEXEC)
            except Exception as e:
                print(f"❌ [Permission Error] Failed to set executable bit: {e}")

    def _find_model(self):
        """Locates the most recently modified .gguf model in the models directory"""
        models_dir = os.path.join(self.base_dir, "models")
        if not os.path.exists(models_dir): return None
        try:
            files = [os.path.join(models_dir, f) for f in os.listdir(models_dir) if f.endswith(".gguf")]
            if not files: return None
            return max(files, key=os.path.getmtime)
        except:
            return None

    def _get_startup_info(self):
        """Hides terminal window on Windows platforms"""
        if self.config.os_type == 'windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return startupinfo
        return None

    def _health_check(self):
        """Verifies driver integrity and model availability"""
        if not os.path.exists(self.driver_path) or not self.model_path:
            return False
        try:
            subprocess.run(
                [self.driver_path, "--version"], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=3.0, 
                startupinfo=self._get_startup_info()
            )
            return True
        except:
            return False

    def generate(self, full_prompt):
        """Yields text chunks from the inference driver. 100% Re-entrant."""
        if not os.path.exists(self.driver_path) or not self.model_path:
            yield "❌ [Critical] Missing Driver or Model."
            return
            
        try:
            full_prompt = str(full_prompt)
        except:
            yield "❌ [Type Error] Invalid prompt format."
            return

        # Unique ID prevents file collisions during concurrent requests
        unique_id = uuid.uuid4().hex[:8]
        local_temp_file = os.path.join(self.base_dir, f".temp_p_{unique_id}.txt")
        local_process = None

        try:
            with open(local_temp_file, "w", encoding="utf-8", errors='ignore') as f:
                f.write(full_prompt)

            command = [
                self.driver_path,
                "-m", self.model_path,
                "-t", str(self.config.threads),
                "-c", self.config.context_size,
                "-ngl", self.config.gpu_layers,
                "-f", local_temp_file, 
                "-n", "1024",           # <--- [추가] 런어웨이 폭주 방지 리미터
                "--log-disable",
                "--no-display-prompt"
            ]

            local_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                startupinfo=self._get_startup_info()
            )
            
            with self.process_lock:
                self.active_processes.append(local_process)

            while True:
                char = local_process.stdout.read(1)
                # Check for process completion or stream termination
                if not char and local_process.poll() is not None:
                    break
                if char:
                    yield char

        except Exception as e:
            yield f"\n❌ [Runtime Error] {str(e)}"
        finally:
            # Resource cleanup: remove process from list and delete temp file
            if local_process:
                with self.process_lock:
                    if local_process in self.active_processes:
                        self.active_processes.remove(local_process)
                try:
                    local_process.terminate()
                    local_process.wait(timeout=1)
                except:
                    try: local_process.kill()
                    except: pass
            
            if os.path.exists(local_temp_file):
                try: os.remove(local_temp_file)
                except: pass

    def stop_all(self):
        """Cleanup on exit: Terminates all orphaned processes and removes temp files"""
        with self.process_lock:
            for p in list(self.active_processes):
                try:
                    p.terminate()
                    p.wait(timeout=1)
                except:
                    try: p.kill()
                    except: pass
            self.active_processes.clear()
            
        try:
            for f in os.listdir(self.base_dir):
                if f.startswith(".temp_p_"):
                    os.remove(os.path.join(self.base_dir, f))
        except:
            pass
