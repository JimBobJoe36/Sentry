from fileWriter import updateLog
from downloadsMonitor import saveDownloadsFilenames, checkDownloads
import random, os
from time import sleep
import subprocess
import sys
from plyer import notification

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

try:
    import plyer
except ImportError:
    install('plyer')
    try:
        import keyboard
        print("Notification module installed successfully.")
    except ImportError:
        print("Failed to install the notification module.")
        sys.exit(1)
# ---------------Starter Variable Setup---------------
reasons = "Booted Up"
user = os.getlogin()
downloads = os.path.join("C:\\Users", user, "Documents", "Sentry", "secureFiles", "trustedLogs", "downloads.txt")

# Handle first-time run
if not os.path.exists(downloads) or os.stat(downloads).st_size < 2:
    print("[INFO] No trusted downloads file found or file is empty. Saving current downloads state.")
    saveDownloadsFilenames()
else:
    print(f"Welcome back, {user}!")
    checkDownloads()

# ---------------Main Process---------------
while True:
    checkDownloads()
    tick = random.uniform(0.1, 1.0)  # Wait between 0.1s and 1s
    sleep(tick)

    if keyboard.is_pressed(']'):
        updateLog("Powered off")
        break

