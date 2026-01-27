import subprocess, sys

def check_ollama(cli_cmd='ollama'):
    try:
        p = subprocess.run(
            [cli_cmd, 'list'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=8
        )
        return p.returncode == 0 and 'llama3.2:1b' in p.stdout.lower()
    except Exception:
        return False


def ask_ollama_cli(cli_cmd, model_name, prompt, timeout=60):
    try:
        proc = subprocess.run(
            [cli_cmd, 'run', model_name],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout
        )

        out = (proc.stdout or '').strip()
        if not out:
            out = (proc.stderr or '').strip()
        return out or '(no output)'

    except subprocess.TimeoutExpired:
        return '(ollama timeout)'

    except Exception as e:
        return f'(ollama error) {e}'
