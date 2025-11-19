import subprocess
import threading
import time
import signal
import webbrowser
import sys
import os
import logging

BASE_DIR = os.getcwd()
SRC_DIR = os.path.join(BASE_DIR, "src")

REACT_DIR = os.path.join(SRC_DIR, "frontend")
BACKEND_DIR = os.path.join(SRC_DIR, "backend")

processes = []


'''
Function to open the browser on application
launch once React and FastAPI are up and running.
Works cross-platform and on a number of browsers
'''
def open_browser(url):
    time.sleep(2)
    try:
        webbrowser.open(url)
        logging.info(f"[Startup] Browser opened at {url}")
    except Exception as e:
        logging.info(f"[Startup] Failed to open the browser: {e}")

'''
Starts up the React frontend to be called by the open_browser
function
'''
def start_react():
    command = ["npm", "start"]
    
    # Windows: shell=True 
    p = subprocess.Popen(command, cwd = REACT_DIR, shell=(os.name == "nt"))
    processes.append(p)
'''
Starts up FastAPI so the frontend and backend can communicate
'''
def start_fastapi():
    command = ["uvicorn", "app:app", "--reload", "--port", "8000"]
    p = subprocess.Popen(
        command,
        cwd=REACT_DIR,
        shell=(os.name == "nt")
    )

def shutdown(*args):
    logging.info("\nShutting down all processes")
    for p in processes:
        try: 
            p.terminate()
        except Exception:
            pass
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)

    logging.info("[Startup] Starting React dev")
    threading.Thread(target=start_react).start()
    
    threading.Thread(target=open_browser, args = ("http://localhost:3000",)).start()

    time.sleep(1.5)

    logging.info("[Startup] Starting FastAPI")
    threading.Thread(target=start_fastapi).start()

    print("Frontend located at http://localhost:3000, window should have launched.")

    while True:
        time.sleep(1)
