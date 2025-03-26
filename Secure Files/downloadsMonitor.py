import os
import getpass
from fileWriter import updateLog
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
    files = os.listdir(downloads_path)
    downloads = open("C://Users/" + user + "/Documents/Sentry/Secure Files/trustedLogs/downloads.txt")
    if files != downloads:
        print("It appears you have downloaded a new file, or have had a file moved from downloads.")
        x = input("Do you want to update downloads.txt? [Y] or [N]")
        if x == "Y" or x == "y":
            save_downloads_filenames()
    downloads.close()
    