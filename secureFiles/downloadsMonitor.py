import os
import getpass
import subprocess
from fileWriter import updateLog

reasons = "Changed Download"

def get_file_hash(filepath, algorithm="SHA256"):
    try:
        # Wrap filepath in double quotes to prevent issues with apostrophes
        result = subprocess.run(
            ["powershell", "-Command", f'Get-FileHash -Path "{filepath}" -Algorithm {algorithm} | Select-Object -ExpandProperty Hash'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error computing hash for {filepath}: {e}")
        return None


def save_downloads_filenames():
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    save_path = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "trustedLogs", "downloads.txt")
    
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        files = os.listdir(downloads_path)
        
        with open(save_path, "w", encoding="utf-8") as file:
            for filename in files:
                file_path = os.path.join(downloads_path, filename)
                if os.path.isfile(file_path):
                    file_hash = get_file_hash(file_path)
                    if file_hash:
                        file.write(f"{filename},{file_hash}\n")
        
        print("Downloads saved.")
        updateLog(reasons)
    except Exception as e:
        print(f"An error occurred: {e}")

def checkDownloads():
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    save_path = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "trustedLogs", "downloads.txt")
    
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            saved_files = {}
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    saved_files[parts[0]] = parts[1]
        
        current_files = {f: get_file_hash(os.path.join(downloads_path, f)) for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))}
        
        if saved_files != current_files:
            print("It appears you have downloaded a new file or a file has been modified/moved.")
            x = input("Do you want to update downloads.txt? [Y] or [N] ")
            if x.lower() == "y":
                save_downloads_filenames()
    except FileNotFoundError:
        print("downloads.txt not found. Creating a new one.")
        save_downloads_filenames()
