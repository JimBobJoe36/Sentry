from fileWriter import updateLog
from downloadsMonitor import save_downloads_filenames, checkDownloads
import getpass, random, os, keyboard
from time import sleep

reasons = "Booted Up"
user = os.getlogin()
downloads = os.path.join("C:\\Users", user, "Documents", "Sentry", "Secure Files", "trustedLogs", "downloads.txt")
downloads_size = os.stat(downloads).st_size
tick = random.randint(0, 100) / 100

# Boot-up
updateLog(reasons)

if downloads_size < 2:
    save_downloads_filenames()
else:
    print("Welcome back", user + "!")
    print("Please wait, as we are checking the downloads... This may take a while.")
    checkDownloads()

while True:
    print("Please wait, as we are checking the downloads... This may take a while.")
    checkDownloads()
    sleep(tick)
    tick = random.randint(0, 100) / 100
    
    if keyboard.is_pressed(']'):  # Checks if the key is pressed
        print("Exit key detected, shutting down.")  # Debug message
        break  # Exit loop

