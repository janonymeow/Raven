import subprocess
from pathlib import Path
def run_in_sandbox(script_path, timeout=30):
    if not Path(script_path).exists():
        return False, 'Script not found.'
    try:
        proc = subprocess.run(['python', str(script_path)], capture_output=True, text=True, timeout=timeout)
        return True, proc.stdout + '\n' + proc.stderr
    except subprocess.TimeoutExpired:
        return False, 'Timeout expired.'
    except Exception as e:
        return False, str(e)
