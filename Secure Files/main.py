import os
from fileWriter import updateLog
from downloadsMonitor import save_downloads_filenames, checkDownloads
import getpass

reasons = "booted up"
user = os.getlogin()
downloads = os.path.join("C:\\Users", user, "Documents", "Sentry", "Secure Files", "trustedLogs", "downloads.txt")
downloads_size = os.stat(downloads).st_size
# Procedures

#Code
updateLog(reasons)
if downloads_size == 0:
    save_downloads_filenames()
else:
    checkDownloads()
