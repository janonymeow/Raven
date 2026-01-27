import os, subprocess
from pathlib import Path

def load_whitelist(cfg):
    return cfg.get('app_whitelist', {})

def find_app_key(app_name, whitelist):
    key = app_name.lower().strip()
    if key in whitelist:
        return key
    for k in whitelist:
        if key in k.lower():
            return k
    return None

def launch_app_by_name(name, whitelist):
    key = find_app_key(name, whitelist)
    if not key:
        return False, f"App '{name}' not found in whitelist."
    path = whitelist[key]
    p = Path(path)
    if not p.exists():
        return False, f"Executable not found at {path}. Update config.yaml."
    try:
        if os.name == 'nt':
            os.startfile(str(path))
        else:
            subprocess.Popen([str(path)])
        return True, f"Launched '{key}'."
    except Exception as e:
        return False, f"Failed to launch '{key}': {e}"
