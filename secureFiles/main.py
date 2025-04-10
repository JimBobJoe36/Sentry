from fileWriter import updateLog
from downloadsMonitor import save_downloads_filenames, checkDownloads
import getpass, random, os
from time import sleep
import subprocess
import sys
# -------------Keyboard Installation Process--------------------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import keyboard
except ImportError:
    install('keyboard')
    try:
        import keyboard
        print("Keyboard module installed successfully.")
    except ImportError:
        print("Failed to install the keyboard module.")
        sys.exit(1)
# ---------------Starter Variable Setup---------------
reasons = "Booted Up"
user = os.getlogin()
downloads = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "trustedLogs", "downloads.txt")
downloads_size = os.stat(downloads).st_size
tick = random.randint(0, 100) / 100

# ---------------Boot-up---------------
updateLog(reasons)

if downloads_size < 2:
    save_downloads_filenames()
else:
    print("Welcome back", user + "!")
    checkDownloads()
# ---------------Main Process---------------
while True:
    checkDownloads()
    sleep(tick)
    tick = random.randint(0, 100) / 100
    
    if keyboard.is_pressed(']'):
        break
