import subprocess
import os

python_exe = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')
try:
    # Try to run server for a few seconds and catch output
    process = subprocess.Popen([python_exe, 'manage.py', 'runserver'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True)
    stdout, stderr = process.communicate(timeout=5)
    print("STDOUT:", stdout)
    print("STDERR:", stderr)
except subprocess.TimeoutExpired:
    process.kill()
    stdout, stderr = process.communicate()
    print("STDOUT (Timed Out):", stdout)
    print("STDERR (Timed Out):", stderr)
except Exception as e:
    print("Error:", e)
