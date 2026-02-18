# ⚙️ BASIC: The Industrial Core Engine

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/Dependencies-ZERO-success.svg)]()

> **"Stop fighting with frameworks. Just start the engine."**

**BASIC** is an industrial-grade, ultra-lightweight inference engine for local LLMs (GGUF). It is designed to act as the flawless internal combustion engine for your AI applications. 

No bloated frameworks. No hidden background services. **Just one Python file and zero external dependencies.**

## 🛡️ Core Philosophy

Modern AI tooling is filled with heavy abstractions and fragile dependencies (`pip install`-heavy). BASIC takes a different approach:
* **Zero Dependency:** Built purely on the Python Standard Library. No `requests`, no `langchain`, no `torch`.
* **Stateless by Design:** BASIC does not remember conversations. It takes a prompt, yields tokens, and cleans up. Memory leaks are impossible.
* **Auto-Tuning:** Automatically detects your OS, CPU cores, and system architecture to calculate the optimal thread count and execution parameters.
* **Hackable:** It is a single file (`basic.py`). You are encouraged to open it, read it, and modify it for your exact needs.

## 🚀 Quick Start (Standalone Mode)

You can run BASIC right out of the box to test your models.

**1. Prepare the Chassis**
Ensure your directory looks like this:

    BASIC/
    ├── drivers/           # Drop your binary here (e.g., llama-cli.exe or llama-cli)
    ├── models/            # Drop your .gguf model here
    └── basic.py           # The Engine

**2. Ignite**
```bash
python basic.py

BASIC will automatically find the first .gguf file in the models folder, detect your hardware, and start the inference stream.

🧩 How to Use as a Library (Developer Mode)
BASIC is designed to be imported into your own projects (like building your own UI, API server, or automated scripts).

from basic import BasicEngine

# 1. Initialize the engine (Auto-detects hardware and models)
engine = BasicEngine()

# 2. Prepare your prompt
prompt = "System: You are a helpful assistant.\nUser: Explain quantum computing in one sentence.\nAssistant:"

# 3. Ignite and stream the output
for token in engine.generate(prompt):
    print(token, end="", flush=True)


🏗️ Architecture (The KapitalSP Ecosystem)
BASIC is the foundational layer. If you are looking for a ready-to-use application with a UI and memory management, check out our derivative projects:

VOID: The Universal AI Chassis (Personal UI wrapping the BASIC engine).

HIVE: The Swarm Node (Networked distributed inference using BASIC).

⚖️ License
Distributed under the Apache License 2.0. See LICENSE for more information.
