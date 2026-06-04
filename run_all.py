import subprocess
import os
import sys
import time
import webbrowser
import socket
from concurrent.futures import ThreadPoolExecutor

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_backend():
    print("[STARTING] Starting Backend Server (Flask)...")
    # Using sys.executable to ensure we use the same python environment
    return subprocess.Popen([sys.executable, "backend/app.py"], 
                            cwd=os.getcwd(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True)

def run_frontend():
    print("[STARTING] Starting Frontend Server (HTTP)...")
    return subprocess.Popen([sys.executable, "-m", "http.server", "8000"], 
                            cwd="frontend",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True)

def monitor_process(name, process):
    for line in iter(process.stdout.readline, ''):
        print(f"[{name}] {line.strip()}")

def main():
    print("=" * 60)
    print("*** RESTAURANT RECOMMENDATION SYSTEM - UNIFIED RUNNER ***")
    print("=" * 60)
    
    # 1. Prerequisite Checks
    print("[CHECK] Checking prerequisites...")
    
    # Check MySQL
    try:
        with socket.create_connection(("localhost", 3306), timeout=2):
            print("[OK] MySQL Service: Running")
    except:
        print("[ERROR] MySQL Service: Not found on port 3306. Please start MySQL.")
        # We'll continue anyway and let the app's own health checks handle it
    
    # Check MongoDB
    try:
        with socket.create_connection(("localhost", 27017), timeout=2):
            print("[OK] MongoDB Service: Running")
    except:
        print("[ERROR] MongoDB Service: Not found on port 27017. Please start MongoDB.")

    # 2. Start Servers
    processes = []
    
    if is_port_in_use(5000):
        print("[WARNING] Port 5000 (Backend) is already in use. Assuming it's already running.")
    else:
        backend_proc = run_backend()
        processes.append(("BACKEND", backend_proc))
    
    if is_port_in_use(8000):
        print("[WARNING] Port 8000 (Frontend) is already in use. Assuming it's already running.")
    else:
        frontend_proc = run_frontend()
        processes.append(("FRONTEND", frontend_proc))

    print("\n[WAIT] Waiting for servers to initialize...")
    time.sleep(3)
    
    # 3. Open Browser
    print("\n[OPENING] Opening the application in your browser...")
    webbrowser.open("http://localhost:8000")
    
    print("\n" + "=" * 60)
    print("[OK] SYSTEM IS LIVE!")
    print("- Frontend: http://localhost:8000")
    print("- Backend:  http://localhost:5000")
    print("Press Ctrl+C to stop both servers.")
    print("=" * 60 + "\n")

    # 4. Monitor outputs
    if processes:
        with ThreadPoolExecutor(max_workers=len(processes)) as executor:
            for name, proc in processes:
                executor.submit(monitor_process, name, proc)
    else:
        print("[INFO] No new processes to monitor.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Shutting down servers...")
        for name, proc in processes:
            proc.terminate()
        print("[EXIT] Goodbye!")
    except Exception as e:
        print(f"\n[ERROR] UNEXPECTED ERROR: {e}")
        input("\nPress ENTER to close...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] CRITICAL ERROR: {e}")
        input("\nPress ENTER to close...")
