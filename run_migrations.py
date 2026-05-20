import os
import sys
import subprocess

def run_cmd(cmd, log_file):
    with open(log_file, 'a') as f:
        f.write(f"Running: {cmd}\n")
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        f.write("STDOUT:\n")
        f.write(stdout)
        f.write("\nSTDERR:\n")
        f.write(stderr)
        f.write(f"\nReturn Code: {process.returncode}\n")
    return process.returncode

log_path = 'migration_log.txt'
if os.path.exists(log_path): os.remove(log_path)

base_dir = os.path.dirname(os.path.abspath(__file__))
python_exe = os.path.join(base_dir, 'venv', 'Scripts', 'python.exe')

with open(log_path, 'a') as f:
    f.write(f"Base Directory: {base_dir}\n")
    f.write(f"Python Executable: {python_exe}\n")

# Check if Builder is in models.py
with open(os.path.join(base_dir, 'apps', 'properties', 'models.py'), 'r') as f:
    content = f.read()
    with open(log_path, 'a') as logf:
        if 'class Builder' in content:
            logf.write("Builder model found in models.py\n")
        else:
            logf.write("Builder model NOT found in models.py\n")

# Run makemigrations
rc = run_cmd(f'"{python_exe}" manage.py makemigrations properties', log_path)
if rc == 0:
    # Run migrate
    run_cmd(f'"{python_exe}" manage.py migrate properties', log_path)
else:
    with open(log_path, 'a') as logf:
        logf.write("Makemigrations failed\n")
