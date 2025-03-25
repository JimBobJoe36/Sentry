import os
from fileWriter import updateLog
from downloadsMonitor import save_downloads_filenames, checkDownloads
import getpass

reasons = "booted up"
user = os.getlogin()
downloads = os.path.join("C:\\Users", user, "Documents", "Sentry", "Secure Files", "trustedLogs", "downloads.txt")
downloads_size = os.stat(downloads).st_size
# Procedures
def bootUp():
    global reasons
    global user
    global downloads
    global downloads_size
    updateLog(reasons)
    if downloads_size == 0:
        save_downloads_filenames()
    else:
        print("Welcome back " + user + "!")
        checkDownloads()
        
#Code

