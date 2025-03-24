import os
import getpass

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
    except Exception as e:
        print(f"An error occurred: {e}")
def checkDownloads():
    pass
    user = getpass.getuser()
    downloads_path = os.path.join("C:\\Users", user, "Downloads")
    files = os.listdir(downloads_path)
    