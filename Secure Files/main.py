from fileWriter import updateLog
from downloadsMonitor import save_downloads_filenames, checkDownloads
import getpass, random, os
from time import sleep

reasons = "Booted Up"
user = os.getlogin()
downloads = os.path.join("C:\\Users", user, "Documents", "Sentry", "Secure Files", "trustedLogs", "downloads.txt")
downloads_size = os.stat(downloads).st_size
tick = random.randint(0, 100) / 100
# Procedures


# Boot-up
updateLog(reasons)
if downloads_size == 0:
    save_downloads_filenames()
else:
    print("Welcome back " + user + "!")
    checkDownloads()