RAVEN
================================

Overview
--------
This package turns the RAVEN terminal assistant into a local Jarvis-style system
that uses your installed Ollama + LLaMA3 model (local) as the brain. It includes:
  - Boot ASCII animations 
  - Terminal-driven assistant with live Ollama integration
  - App whitelist launcher and system power commands (shutdown/restart/sleep)
  - Code generation drafts saved to RavenDrafts/
  - Lightweight sandbox execution helper (for running drafts safely)
  - Logging of actions

IMPORTANT
---------
- This package **does not** install Ollama or model files. You already have Ollama and llama3.
- The script calls the `ollama` CLI via subprocess. Ensure `ollama` is in your PATH.
- Review config.yaml and edit app paths and toggles to match your Windows setup.
- Power commands WILL affect your PC. Use with care.

Quick start (Windows)
---------------------
1. Install Python 3.10+.
2. Open PowerShell/CMD in this folder.
3. Install dependencies:
   pip install -r requirements.txt
4. Edit config.yaml to set your username, app paths, and toggles.
5. Run:
   python raven.py

How to install ollama?
----------------------
- Go to "https://ollama.com/download" and download the OllamaSetup.exe
- or maybe you could try `pip install ollama` in your terminal
 for this setup, i embbeded the `llama3.2:1b` (lightweight) but you can modify them
- To install the LLM you can run `ollama run llama3.2:1b` (easiest way)
- You can choose models from "https://ollama.com/search"
- If you choose other models, please modify;
   model_name: llama3.2:1b
      FLoc: config.yaml on Line 2

   MODEL_NAME = cfg.get('model_name', 'llama3.2:1b')
      FLoc: raven.py on Line 113