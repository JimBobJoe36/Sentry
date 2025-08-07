from fileWriter import updateLog
from downloadsMonitor import saveDownloadsFilenames, checkDownloads
import random
import os
from time import sleep
import subprocess
import sys

# -------------Keyboard Installation Process--------------------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


pkgs = ["keyboard", "plyer"]

for pkg in pkgs:
    try:
        install(pkg)
    except Exception as e:
        print(f"Could not install {pkg}: {e}")
        updateLog(f"[Error] Could not install {pkg}")
        sys.exit(1)

# ---------------Starter Variable Setup---------------
updateLog("Booted Up")
user = os.getlogin()
downloads = os.path.join(
    "C:\\Users",
    user,
    "Documents",
    "Sentry",
    "secureFiles",
    "trustedLogs",
    "downloads.txt")

# Handle first-time run
if not os.path.exists(downloads) or os.stat(downloads).st_size < 2:
    print("[INFO] No trusted downloads file found or file is empty."
          "Saving current downloads state.")
    saveDownloadsFilenames()
else:
    print(f"Welcome back, {user}!")
    checkDownloads()

# ---------------Main Process---------------
import keyboard
while True:
    checkDownloads()
    tick = random.uniform(0.1, 1.0)
    sleep(tick)

    if keyboard.is_pressed(']'):
        updateLog("Powered off")
        break
