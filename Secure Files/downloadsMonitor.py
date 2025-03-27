import os
import getpass
from fileWriter import updateLog
import pygetwindow as gw
import win32gui, win32con
reasons = "Changed Download"
def save_downloads_filenames():
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    save_path = os.path.join("C:\\Users", user, "Documents", "Sentry", "Secure Files", "trustedLogs", "downloads.txt")
    
    try:
        # Ensure the target directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Get all file names in the Downloads directory
        files = os.listdir(downloads_path)
        
        # Write file names to the text file
        with open(save_path, "w", encoding="utf-8") as file:
            for filename in files:
                file.write(filename + "\n")
        
        print(f"Downloads saved.")
        updateLog(reasons)
    except Exception as e:
        print(f"An error occurred: {e}")
def checkDownloads():
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    files = set(os.listdir(downloads_path))  # Convert to set for easier comparison

    save_path = os.path.join("C:\\Users", user, "Documents", "Sentry", "Secure Files", "trustedLogs", "downloads.txt")

    try:
        with open(save_path, "r", encoding="utf-8") as f:
            saved_files = set(line.strip() for line in f)  # Read lines, stripping whitespace/newlines

        if files != saved_files:  # Correctly compare sets of filenames
            win32gui.SetForegroundWindow(hwnd)
            print("It appears you have downloaded a new file, or have had a file moved from downloads.")
            x = input("Do you want to update downloads.txt? [Y] or [N] ")
            if x.lower() == "y":
                save_downloads_filenames()

    except FileNotFoundError:
        print("downloads.txt not found. Creating a new one.")
        save_downloads_filenames()
    