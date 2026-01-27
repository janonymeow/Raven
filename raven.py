import os, sys, json, time, datetime, subprocess,yaml
from pathlib import Path
from modules.appcontrol import load_whitelist, launch_app_by_name
from modules.llama_adapter import check_ollama, ask_ollama_cli
from modules.sandbox import run_in_sandbox
from modules.voice import VoiceEngine
from colorama import Fore, Style, init as colorama_init

BASE = Path(__file__).parent
with open(BASE / 'config.yaml', 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

LOGS = BASE / cfg.get('logs_dir', 'logs')
DRAFTS = BASE / cfg.get('drafts_dir', 'RavenDrafts')
LOGS.mkdir(exist_ok=True)
DRAFTS.mkdir(exist_ok=True)
LOGFILE = LOGS / 'raven.log'


def log(msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOGFILE, 'a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')


RED = '\033[91m' if os.name != 'nt' else ''
CYAN = '\033[96m' if os.name != 'nt' else ''
LIME = '\033[92m' if os.name != 'nt' else ''
RESET = '\033[0m' if os.name != 'nt' else ''


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# start
def boot_animation():
    os.system("cls" if os.name == "nt" else "clear")
    logo = r"""
            ⠀⠀⠀⠀                         
                                     ░▓▓▓▒   
                                   ▓▓▓▓      
            ░░░░░░░░░░░░░░░░░  ▓▓▓▓▓▓▓       
         ░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓         
      ░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓░         
     ░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓          
   ░░░░░░░▓░▒▒░░░░░░░░░░░░░▒▓▓▓▓▓▓▓░░        
  ░░░░░░▒▒▓▓▓░▓▓▒▒▓▓░░░░░░░▓▓▓▓▓▓▓░░░░       
  ░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒░░░░░░      
 ░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒░░░░░░░      
 ░░░░░░░░░░░░▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒░░░░░ ░▓▒ 
 ░░░░░░░░░░░░░░░░▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
░░░░░░░░░░░░░░░░░░▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    
 ░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░     
 ░░░░░░░░░░░░░░░░░▓▓▓░░░░░▓▓▓░░░░░░░░░░░     
  ░░░░░░░░░░░░░░░░▓▒░░░░░░░░░░▓░░░░░░░░      
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░       
   ░░░░░░░░░░░░░░░░░░░░░░░░░░▒░░░░░░░        
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░         
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░           
        ░░░░░░░░░░░░░░░░░░░░░░░░             
           ░░░░░░░░░░░░░░░░░░                
                ░░░░░░░░░                    
    """
    print(Fore.RED + logo + Style.RESET_ALL)
    speak("Boot sequence engaged. Initializing RAVEN core...")

    # smooth solid progress bar
    bar_len = 32
    for i in range(bar_len + 1):
        filled = "█" * i
        empty = "-" * (bar_len - i)
        pct = int((i / bar_len) * 100)
        sys.stdout.write(f"\r[{Fore.GREEN}{filled}{Style.RESET_ALL}{empty}] {pct}%")
        sys.stdout.flush()
        time.sleep(0.04 if i < bar_len*0.7 else 0.08)
    print("\n")
    speak("System core initialized. RAVEN online, standing by Part.")

# end

def loading_bar():
    clear()
    print(f"{CYAN}Initializing neural core...{RESET}")
    for i in range(0, 101, 3):
        bar = '█' * (i // 3)
        sys.stdout.write(f"\r{LIME}[{bar:<34}] {i}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.02)
    print('\nBoot sequence complete.')
    time.sleep(0.6)
    clear()


def boot_sequence():
    boot_animation()
    loading_bar()
    print(
        f"{LIME}\n╔═══════════════════════════════════════╗\n║   RAVEN        -    SYSTEM ONLINE     ║\n╚═══════════════════════════════════════╝\n{RESET}")
    log('Boot completed')


APP_WHITELIST = load_whitelist(cfg)
voice = VoiceEngine(enable_tts=cfg.get('enable_tts', True)) if cfg.get('enable_voice', True) else None


def speak(text):
    print(f"{CYAN}RAVEN: {text}")
    if voice:
        voice.speak(text)


OLLAMA_CMD = cfg.get('ollama_cli', 'ollama')
MODEL_NAME = cfg.get('model_name', 'llama3.2:1b')


def model_available():
    if cfg.get('model_backend', 'ollama') != 'ollama':
        return False
    ok = check_ollama(OLLAMA_CMD)
    return ok


def ask_model(prompt):
    if not model_available():
        return f'(local dummy) I received your prompt: {prompt}'
    out = ask_ollama_cli(OLLAMA_CMD, MODEL_NAME, prompt)
    return out


def handle_open(cmd):
    parts = cmd.split(' ', 1)
    if len(parts) < 2:
        speak('Specify an app to open.')
        return
    target = parts[1].strip()
    ok, msg = launch_app_by_name(target, APP_WHITELIST)
    speak(msg)
    log(f'OPEN {target} -> {msg}')


def handle_power(action):
    if not cfg.get('allow_power', True):
        speak('Power commands are disabled in config.')
        return
    speak(f'Confirm: do you want me to {action} the system? Type yes to proceed.')
    confirm = input('Confirm (yes/no) > ').strip().lower()
    if confirm != 'yes':
        speak('Cancelled.')
        return
    speak(f'Executing {action} in 3 seconds.')
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    log(f'POWER {action} executed')
    if action == 'shutdown':
        os.system('shutdown /s /t 0' if os.name == 'nt' else 'shutdown now')
    elif action == 'restart':
        os.system('shutdown /r /t 0' if os.name == 'nt' else 'reboot')
    elif action == 'sleep':
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0'
                  if os.name == 'nt' else 'systemctl suspend')


def handle_generate(cmd):
    parts = cmd.split(' ', 1)
    if len(parts) < 2:
        speak('Please specify a name for the generated draft.')
        return
    title = parts[1].strip().replace(' ', '_')
    filename = f"{int(time.time())}_{title}.py"
    path = DRAFTS / filename
    sample = f"# Auto-generated draft by RAVEN\n# Title: {title}\nprint('Hello from {title}')\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(sample)
    speak(f'Generated draft saved to {path.name} in RavenDrafts.')
    log(f'Generated draft: {path.name}')


def handle_run_draft(cmd):
    parts = cmd.split(' ', 1)
    if len(parts) < 2:
        speak('Specify draft filename to run.')
        return
    filename = parts[1].strip()
    path = DRAFTS / filename
    ok, output = run_in_sandbox(path)
    if ok:
        speak('Script executed. See output below.')
        print(output)
        log(f'Ran draft {filename}')
    else:
        speak(f'Execution failed: {output}')
        log(f'Run failed {filename} -> {output}')


def shutdown_animation():
    clear()
    speak('Shutting down core systems.')
    print('\nInitiating shutdown sequence...\n')
    for i in range(5, 0, -1):
        print(f'Powering down in {i}...')
        time.sleep(1)
    clear()
    if os.name != 'nt':
        for _ in range(20):
            print(''.join(['|' if (i % 3 == 0) else ' ' for i in range(80)]))
            time.sleep(0.02)
    print('\nRAVEN: Neural core offline. Goodbye.')
    if voice:
        voice.speak('Raven offline.')
    log('Shutdown complete.')


def main_loop():
    boot_sequence()
    speak('Entering admin mode. All systems nominal.')
    if not model_available():
        speak('Warning: Ollama/llama3 not detected. Running in dummy fallback.')
    while True:
        try:
            cmd = input('\n > ').strip()
            if not cmd:
                continue
            lc = cmd.lower().strip()
            if lc in ('exit', 'goodnight'):
                speak('Shutting down. Goodbye Part.')
                log('User exit.')
                shutdown_animation()
                break
            if lc.startswith(('open ', 'launch ')):
                handle_open(lc)
                continue
            if lc in ('shutdown', 'restart', 'sleep'):
                handle_power(lc)
                continue
            if lc.startswith('generate '):
                handle_generate(lc)
                continue
            if lc.startswith('run '):
                handle_run_draft(lc)
                continue
            if lc.startswith('speak '):
                text = cmd.split(' ', 1)[1]
                speak(text)
                continue
            if lc == 'listen':
                if voice:
                    speak('Listening now...')
                    txt, err = voice.listen_once()
                    if txt:
                        print('Heard >', txt)
                        speak('Got it.')
                    else:
                        speak(f'Listen failed: {err}')
                else:
                    speak('Voice disabled in config.')
                continue
            speak('RAVEN is thinking...')
            response = ask_model(cmd)
            print('\nRAVEN >\n', response)
            log(f'MODEL QUERY: {cmd} -> {len(response)} chars')
        except KeyboardInterrupt:
            speak('Interrupted. speak shutdown to exit cleanly.')
        except Exception as e:
            print('Error:', e)
            log(f'ERROR: {e}')


if __name__ == '__main__':
    main_loop()
