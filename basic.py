import os, sys, subprocess, platform, threading, queue, time

# ==============================================================================
# ⚡ BASIC v3.0 [OVERCLOCK]
# Zero Dependency | Multi-Threaded | Flash Attention | H/W Accelerated
# ==============================================================================

# [System Spec Auto-Detection]
CORES = os.cpu_count() or 4
IS_MOBILE = 'termux' in str(os.environ) or 'android' in str(os.environ)

# [Performance Flags]
# -t: CPU 쓰레드 풀가동
# -ngl: GPU 가속 최대치
# -fa: 플래시 어텐션 (속도 향상)
# --no-mmap: 램에 강제 로딩 (로딩 느림, 실행 빠름)
FLAGS = ["-t", str(CORES), "-ngl", "999", "-fa", "-c", "4096", "-b", "512", "--log-disable"]

class Engine:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.driver = self._get_driver()
        self.model = self._get_model()
        self.q = queue.Queue()
        self.proc = None

    def _get_driver(self):
        if IS_MOBILE: return "llama-cli"
        sys_os = platform.system()
        b = "llama-cli.exe" if sys_os=='Windows' else "llama-cli-mac" if sys_os=='Darwin' else "llama-cli-linux"
        return os.path.join(self.root, 'drivers', b)

    def _get_model(self):
        mdir = os.path.join(os.environ.get('HOME','.'), 'models') if IS_MOBILE else os.path.join(self.root, 'models')
        try: return os.path.join(mdir, [f for f in os.listdir(mdir) if f.endswith('.gguf')][0])
        except: return None

    def _reader(self, stream):
        """백그라운드 스레드: 출력을 실시간으로 낚아채서 큐에 넣음"""
        for line in iter(stream.readline, ''):
            self.q.put(line)
        stream.close()

    def generate(self, prompt):
        if not self.model: return print(" [!] Error: No model file found.")
        
        cmd = [self.driver, "-m", self.model, "-p", f"User: {prompt}\nAssistant:"] + FLAGS
        
        # 프로세스 생성 (비동기)
        self.proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding='utf-8', errors='replace', bufsize=1
        )

        # 별도 스레드가 출력을 감시함 (메인 스레드 안 멈춤)
        t = threading.Thread(target=self._reader, args=(self.proc.stdout,))
        t.daemon = True # 메인 프로그램 죽으면 같이 죽음
        t.start()

        print(" VOID: ", end="", flush=True)

        # 메인 루프: 큐에서 데이터를 꺼내서 출력
        while self.proc.poll() is None or not self.q.empty():
            try:
                line = self.q.get(timeout=0.01) # 0.01초 대기 (CPU 과부하 방지)
                print(line, end="", flush=True)
            except queue.Empty:
                continue
        print("\n")

def main():
    if IS_MOBILE: os.system("clear")
    else: os.system("cls" if os.name=='nt' else "clear")

    print(f" [SYSTEM] Cores: {CORES} | GPU Layers: Max | Flash Attn: ON")
    print(f" [BASIC] Multi-Threaded Engine Ready.\n")

    engine = Engine()
    
    while True:
        try:
            p = input(" You: ").strip()
            if not p: continue
            if p.lower() in ['exit', 'quit']: break
            engine.generate(p)
        except KeyboardInterrupt:
            print("\n [!] Interrupted.")
            break

if __name__ == "__main__":
    main()
