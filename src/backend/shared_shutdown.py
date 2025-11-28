import logging

process_list = []

def setprocesses(processes):
    process_list = processes

# Shutdown function similar to the one in the run.py, but included here to allow
# routes.py to shutdown the function when the UI tells it to.
def shutdown(*args):
    logging.info("\nShutting down all processes")
    for p in processes:
        try: 
            p.terminate()
        except Exception:
            pass
    sys.exit(0)