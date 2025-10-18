import os
import zipfile
import subprocess
import tempfile
import gdown
from utils import log

# --- WinRAR Extraction Function (Minor fix) ---

def extract_with_winrar(rar_path, extract_to):
    """
    Attempts to extract a RAR file using the WinRAR command-line utility.
    """
    possible_paths = [
        r"C:\Program Files\WinRAR\WinRAR.exe",
        r"C:\Program Files (x86)\WinRAR\WinRAR.exe"
    ]
    winrar_path = None
    for path in possible_paths:
        # Check if the path exists (case-insensitive on Windows)
        if os.path.exists(path):
            winrar_path = path
            break
    if not winrar_path:
        # NOTE: Consider using 'unrar' if available via PATH for non-Windows or if WinRAR is not preferred.
        log("⚠️ WinRAR not found. Please install it or ensure it's in a standard location.")
        return False

    os.makedirs(extract_to, exist_ok=True)
    log(f"📦 Extracting with WinRAR: {os.path.basename(rar_path)}")

    try:
        # Use 'e' (Extract to current directory or one specified) instead of 'x' (Extract with full paths)
        # to ensure files are placed directly into extract_to if the archive has a single root folder.
        # '-y' is for yes to all.
        subprocess.run(
            [winrar_path, "e", "-y", rar_path, extract_to],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log("🗂️ RAR file extracted successfully with WinRAR.")
        return True
    except subprocess.CalledProcessError as e:
        log(f"❌ WinRAR extraction failed (code {e.returncode}). Check if the file is valid or password-protected.")
        return False

# --- Website Setup Function (Major Fixes) ---

def setup_website(htdocs_dir):
    """
    Downloads a website package from Google Drive and extracts it to the htdocs directory.
    """
    try:
        if not htdocs_dir:
            log("❌ Invalid htdocs directory. Directory path cannot be empty.")
            return False

        # Preset Google Drive file ID
        file_id = "1y0B90opHvIRQIpCsHLGgKh_J-v4-8Oqk" # Assuming this ID points to a .zip or .rar
        
        # 1. Use tempfile.NamedTemporaryFile to ensure a unique, correctly closed file handle
        # and let gdown determine the actual filename/extension if possible, or use a generic name.
        # Note: gdown often saves files without an extension if the original filename isn't available.
        temp_dir = tempfile.gettempdir()
        
        # We will let gdown name the file and then check the result.
        temp_file_name = "website_package_download" # Generic base name
        file_path_base = os.path.join(temp_dir, temp_file_name) 
        
        # Google Drive URL for download
        url = f"https://drive.google.com/uc?id={file_id}" 

        log(f"🌐 Downloading website package from Google Drive ID: {file_id}")
        
        # Use gdown.download, ensuring a proper path is returned
        # 'fuzzy=False' is correct. 'quiet=False' helps see gdown progress.
        # 'output' parameter is used to specify the output path. gdown will append
        # the Google Drive filename if available, or use this path.
        downloaded_file_path = gdown.download(
            url, 
            output=file_path_base, 
            quiet=False, 
            fuzzy=False
        )
        
        if not downloaded_file_path or not os.path.exists(downloaded_file_path):
            log("❌ Failed to download the website package. Check file ID or network connection.")
            return False

        # Use the actual path returned by gdown for logging and processing
        file_path = os.path.abspath(downloaded_file_path)
        log(f"✅ Downloaded to: {file_path}")

        # Check for potential Google Drive warning/HTML page
        # The log shows the downloaded file path is 'C:\Users\TGR.H\AppData\Local\Temp\website_package'
        # which strongly suggests gdown failed to get the archive and instead got an HTML warning page
        # or a temporary redirect file.
        
        # 2. Robust file type detection (rely on signature, not extension)
        try:
            with open(file_path, "rb") as f:
                sig = f.read(10) # Read more bytes for better signature matching
        except Exception as file_read_error:
            log(f"❌ Could not read downloaded file: {file_read_error}")
            return False
            
        # Define extraction target
        site_path = os.path.abspath(htdocs_dir)
        os.makedirs(site_path, exist_ok=True)
        
        # ZIP signature: PK\x03\x04
        # RAR signature: Rar!\x1a\x07\x00 (for RAR 5.0) or Rar!\x1a\x07\x01\x00 (for RAR 4.x)
        if sig.startswith(b"PK\x03\x04") or sig.startswith(b"PK\x05\x06"): # Added check for empty ZIP signature
            log("📦 Detected and Extracting ZIP file...")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(site_path)
            log("🗂️ ZIP file extracted successfully.")
        elif sig[:7] == b"Rar!\x1a\x07\x00" or sig[:7] == b"Rar!\x1a\x07\x01":
            log("📦 Detected RAR file. Attempting extraction with WinRAR...")
            if not extract_with_winrar(file_path, site_path):
                return False
        else:
            # Check for common HTML response (a sign of a large file warning page)
            if b"<!DOCTYPE html" in sig or b"<html" in sig or b"Google Drive" in sig:
                 log("⚠️ Downloaded file is likely an HTML page (Google Drive Warning).")
                 log("    The file might be too large and requires manual confirmation in a browser.")
            else:
                 log(f"⚠️ Unsupported file format. Signature: {sig.hex()}")
                 log("    Ensure the Google Drive ID is correct and points directly to an archive.")
            return False

        log(f"✅ Website extracted successfully to: {site_path}")
        return True

    except gdown.exceptions.GDownException as gde:
        log(f"❌ gdown failed: {gde}")
        return False
    except Exception as e:
        import traceback
        log(f"❌ Website setup failed: {e}\n{traceback.format_exc()}")
        return False

# NOTE ON GDOWN:
# If the file is very large, gdown might fail because Google Drive requires a confirmation
# page to be clicked (the "Google Drive can't scan this file for viruses" warning).
# The downloaded file in this case is the HTML warning page, which is not a ZIP/RAR file.
# You can try passing 'use_cookies=False' (or use a different download method) if this is the case.