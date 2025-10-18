import subprocess
import os
from utils import log

server_process = None

def start_server():
    global server_process
    try:
        if not os.path.exists("website"):
            os.makedirs("website", exist_ok=True)
        log("Starting Python HTTP server...")
        server_process = subprocess.Popen(["python", "-m", "http.server", "8080"], cwd="website")
        return True
    except Exception as e:
        log(f"Error starting server: {e}")
        return False

def stop_server():
    global server_process
    try:
        if server_process:
            server_process.terminate()
            log("Server process terminated.")
            server_process = None
            return True
        else:
            log("No server running to stop.")
            return False
    except Exception as e:
        log(f"Error stopping server: {e}")
        return False
