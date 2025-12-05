import logging
import sys
import os
import subprocess

process_list = []

def setprocesses(processes):
    global process_list
    process_list = processes

# Shutdown function similar to the one in the run.py, but included here to allow
# routes.py to shutdown the function when the UI tells it to.
def shutdown(*args):
    logging.info("\nShutting down all processes")

    # On Windows, need to kill the entire process tree
    if os.name == "nt":
        for p in process_list:
            try:
                # Use taskkill to kill process tree on Windows
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)],
                              stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except Exception as e:
                logging.error(f"Error killing process {p.pid}: {e}")
    else:
        # On Unix-like systems, terminate normally
        for p in process_list:
            try:
                p.terminate()
            except Exception:
                pass

    sys.exit(0)