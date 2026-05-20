import os
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    with open('migration_result.txt', 'a') as f:
        f.write(f"Command: {cmd}\n")
        f.write(f"STDOUT: {result.stdout}\n")
        f.write(f"STDERR: {result.stderr}\n")
        f.write(f"Return Code: {result.returncode}\n")
    return result.returncode

python_exe = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')

run_cmd(f'"{python_exe}" manage.py migrate properties')
