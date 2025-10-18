import platform
import subprocess
from utils import log

def install_dependencies():
    try:
        os_type = platform.system().lower()
        log(f"Detected OS: {os_type}")

        if "windows" in os_type:
            subprocess.run(["python", "-m", "ensurepip"], check=False)
            subprocess.run(["pip", "install", "--upgrade", "pip"], check=False)
            log("Pip ensured and upgraded.")
        elif "linux" in os_type:
            subprocess.run(["sudo", "apt-get", "update"], check=False)
            subprocess.run(["sudo", "apt-get", "install", "-y", "apache2"], check=False)
            log("Apache installed on Linux.")
        else:
            log("Unsupported OS.")
            return False
        return True
    except Exception as e:
        log(f"Error installing dependencies: {e}")
        return False
