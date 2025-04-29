import subprocess
import time
import threading
import os

# getting the absolute paths for flask servers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_PATH = os.path.join(BASE_DIR, "home.py")
CHATBOT_PATH = os.path.join(BASE_DIR, "chatbot.py")

# using global process for reference
processes = {}

def launch_process(name, path):
    print(f"[{name}] Starting...")
    return subprocess.Popen(["python", path])

def monitor_process(name, path, restart_interval=None):
    while True:
        proc = launch_process(name, path)
        processes[name] = proc
        start_time = time.time()

        while True:
            try:
                proc.wait(timeout=5)
                print(f"[{name}] Crashed. Restarting...")
                break  # restart when crashing occurs
            except subprocess.TimeoutExpired:
                # check if it's time for home.py to restart
                if restart_interval and (time.time() - start_time > restart_interval):
                    print(f"[{name}] Hourly restart. Restarting...")
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    break

def main():
    # start home.py
    threading.Thread(target=monitor_process, args=("home", HOME_PATH, 3600), daemon=True).start()

    # start chatbot.py
    threading.Thread(target=monitor_process, args=("chatbot", CHATBOT_PATH), daemon=True).start()

    # keep main thread alive
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
