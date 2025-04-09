import os
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
            saved_files = {}
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    saved_files[parts[0]] = parts[1]
        
        current_files = {}
        with ThreadPoolExecutor() as executor:
            file_hashes = executor.map(lambda filename: (filename, get_file_hash(os.path.join(downloads_path, filename))),
                                       [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))])
            for filename, file_hash in file_hashes:
                if file_hash:
                    current_files[filename] = file_hash
        
        if saved_files != current_files:
            print("It appears you have downloaded a new file or a file has been modified/moved.")
            inp = input("Would you like to see the new files/filhashes? [Y] or [N]")
            if inp.lower() == "y":
                for i in current_files:
                    if i not in saved_files:
                        differences.append(current_files[i])
                print(differences)
                print("To compare, open up downloads.txt")
            x = input("Do you want to update downloads.txt? [Y] or [N] ")
            if x.lower() == "y":
                save_downloads_filenames()
    except FileNotFoundError:
        print("downloads.txt not found. Creating a new one.")
        save_downloads_filenames()

