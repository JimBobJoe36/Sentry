'''import os
import getpass
import hashlib
from concurrent.futures import ThreadPoolExecutor
from fileWriter import updateLog
inp = ""
differences = []
reasons = "Changed Download"

def get_file_hash(filepath, algorithm="sha256"):
    try:
        hash_func = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
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
            with ThreadPoolExecutor() as executor:
                file_hashes = executor.map(lambda filename: (filename, get_file_hash(os.path.join(downloads_path, filename))),
                                           [f for f in files if os.path.isfile(os.path.join(downloads_path, f))])
                for filename, file_hash in file_hashes:
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
            savedFiles = {}
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    savedFiles[parts[0]] = parts[1]
        
        currentFiles = {}
        with ThreadPoolExecutor() as executor:
            file_hashes = executor.map(lambda filename: (filename, get_file_hash(os.path.join(downloads_path, filename))),
                                       [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))])
            for filename, file_hash in file_hashes:
                if file_hash:
                    currentFiles[filename] = file_hash
        if savedFiles != currentFiles:
            print("It appears you have downloaded a new file or a file has been modified/moved.")
            inp = input("Would you like to see the new files/filhashes? [Y] or [N] ")
# Getting the differences between the two...
            if inp.lower() == "y":
                for i in currentFiles:
                    if i not in savedFiles:
                        differences.append(i)
                for i in savedFiles:
                    if i not in currentFiles:
                        differences.append(i)
                print(differences)
                print("To compare, open up downloads.txt")
            x = input("Do you want to update downloads.txt? [Y] or [N] ")
            if x.lower() == "y":
                save_downloads_filenames()
    except FileNotFoundError:
        print("downloads.txt not found. Creating a new one.")
        save_downloads_filenames()'''

import os
import getpass
import hashlib
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
from fileWriter import updateLog

inp = ""
differences = []
reasons = "Changed Download"

def get_file_hash(filepath, algorithm="sha256"):
    try:
        hash_func = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"Error computing hash for {filepath}: {e}")
        return None

def zip_file(filepath, zip_dir):
    os.makedirs(zip_dir, exist_ok=True)
    filename = os.path.basename(filepath)
    zip_path = os.path.join(zip_dir, f"{filename}.zip")
    with ZipFile(zip_path, 'w') as zipf:
        zipf.write(filepath, arcname=filename)
    print(f"[INFO] Zipped {filename} to {zip_path}")
    os.remove(filepath)
    print(f"[INFO] Removed original file: {filename}")
    return zip_path

def unzip_file(zip_path, extract_dir):
    with ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)
    print(f"[INFO] Restored file from {zip_path}")

def save_downloads_filenames():
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    save_path = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "trustedLogs", "downloads.txt")

    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        files = os.listdir(downloads_path)

        with open(save_path, "w", encoding="utf-8") as file:
            with ThreadPoolExecutor() as executor:
                file_hashes = executor.map(lambda filename: (filename, get_file_hash(os.path.join(downloads_path, filename))),
                                           [f for f in files if os.path.isfile(os.path.join(downloads_path, f))])
                for filename, file_hash in file_hashes:
                    if file_hash:
                        file.write(f"{filename},{file_hash}\n")

        print("[INFO] Downloads saved.")
        updateLog(reasons)
    except Exception as e:
        print(f"An error occurred: {e}")

def checkDownloads():
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    zip_dir = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "zippedDownloads")
    save_path = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "trustedLogs", "downloads.txt")

    try:
        with open(save_path, "r", encoding="utf-8") as f:
            savedFiles = {}
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    savedFiles[parts[0]] = parts[1]

        currentFiles = {}
        with ThreadPoolExecutor() as executor:
            file_hashes = executor.map(lambda filename: (filename, get_file_hash(os.path.join(downloads_path, filename))),
                                       [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))])
            for filename, file_hash in file_hashes:
                if file_hash:
                    currentFiles[filename] = file_hash

        if savedFiles != currentFiles:
            print("[NOTICE] New or changed downloads detected.")
            inp = input("Show differences? [Y/N]: ")
            if inp.lower() == "y":
                for i in currentFiles:
                    if i not in savedFiles:
                        differences.append(i)
                for i in savedFiles:
                    if i not in currentFiles:
                        differences.append(i)
                print("Changed files:", differences)

            # Zip and remove new/changed files
            for filename in differences:
                full_path = os.path.join(downloads_path, filename)
                if os.path.exists(full_path):
                    zip_file(full_path, zip_dir)

            # Unzip all files back if user approves
            restore = input("Restore (unzip) all secured files back to Downloads? [Y/N]: ")
            if restore.lower() == "y":
                for zfile in os.listdir(zip_dir):
                    if zfile.endswith(".zip"):
                        unzip_file(os.path.join(zip_dir, zfile), downloads_path)

            x = input("Update downloads.txt with new file states? [Y/N]: ")
            if x.lower() == "y":
                save_downloads_filenames()

    except FileNotFoundError:
        print("[WARN] downloads.txt not found. Creating a new one.")
        save_downloads_filenames()
