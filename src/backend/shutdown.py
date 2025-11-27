import logging

processes = []

def setprocesses(processes):
    self.processes = processes

def shutdown(*args):
    logging.info("\nShutting down all processes")
    for p in processes:
        try: 
            p.terminate()
        except Exception:
            pass
    sys.exit(0)