import os
import subprocess
import time

python_exe = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')
process = subprocess.Popen([python_exe, 'manage.py', 'runserver'], stdout=open('server_stdout.txt', 'w'), stderr=open('server_stderr.txt', 'w'))
time.sleep(5)
print(f"Server started with PID: {process.pid}")
