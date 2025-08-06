import os
import getpass
import hashlib
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
from fileWriter import updateLog
from plyer import notification

inp = ""
differences = []
reasons = "Changed Download"


def getFileHash(filepath, algorithm="sha256"):
    try:
        hashFunc = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hashFunc.update(chunk)
        return hashFunc.hexdigest()
    except Exception as e:
        print(f"Error computing hash for {filepath}: {e}")
        return None


def zipFile(filepath, zipDir):
    os.makedirs(zipDir, exist_ok=True)
    filename = os.path.basename(filepath)
    zip_path = os.path.join(zipDir, f"{filename}.zip")
    with ZipFile(zip_path, 'w') as zipf:
        zipf.write(filepath, arcname=filename)
    print(f"[INFO] Zipped {filename} to {zip_path}")
    os.remove(filepath)
    print(f"[INFO] Removed original file: {filename}")
    return zip_path


def sendNotification(header, messContent):
    notification.notify(
        title=header,
        message=messContent,
        timeout=10
    )


def unzipFile(zip_path, extract_dir):
    with ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)
    print(f"[INFO] Restored file from {zip_path}")


def saveDownloadsFilenames():
    user = getpass.getuser()
    downloadsPath = os.path.join("C:\\Users", user, "Downloads")
    savePath = os.path.join(
        "C:\\Users",
        user,
        "Documents",
        "Sentry",
        "secureFiles",
        "trustedLogs",
        "downloads.txt"
    )

    try:
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        files = os.listdir(downloadsPath)

        with open(savePath, "w", encoding="utf-8") as file:
            with ThreadPoolExecutor() as executor:
                fileHashes = executor.map(lambda filename: (
                    filename,
                    getFileHash(os.path.join(downloadsPath, filename))),
                                          [f for f in files if os.path.isfile(
                                              os.path.join(downloadsPath, f)
                                            )])
                for filename, file_hash in fileHashes:
                    if file_hash:
                        file.write(f"{filename},{file_hash}\n")

        print("[INFO] Downloads saved.")
        updateLog(reasons)
    except Exception as e:
        print(f"An error occurred: {e}")


def checkDownloads():
    user = getpass.getuser()
    downloadsPath = os.path.join("C:\\Users", user, "Downloads")
    zipDir = os.path.join(
        "C:\\Users",
        user,
        "Documents",
        "Sentry",
        "secureFiles",
        "zippedDownloads"
    )
    savePath = os.path.join(
        "C:\\Users",
        user,
        "Documents",
        "Sentry",
        "secureFiles",
        "trustedLogs",
        "downloads.txt"
    )

    try:
        with open(savePath, "r", encoding="utf-8") as f:
            savedFiles = {}
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    savedFiles[parts[0]] = parts[1]

        currentFiles = {}
        with ThreadPoolExecutor() as executor:
            fileHashes = executor.map(
                lambda filename: (
                    filename,
                    getFileHash(
                        os.path.join(
                            downloadsPath,
                            filename
                        ))),
                [f for f in os.listdir(downloadsPath) if
                    os.path.isfile(os.path.join(downloadsPath, f))])
            for filename, file_hash in fileHashes:
                if file_hash:
                    currentFiles[filename] = file_hash

        if savedFiles != currentFiles:
            print("[INFO] New or changed downloads detected.")

            sendNotification("[INFO] Action Needed",
                             "We found new files in your downloads, "
                             "please interact with Sentry.")
            updateLog("Notification sent")

            for i in currentFiles:
                if i not in savedFiles:
                    differences.append(i)
            for i in savedFiles:
                if i not in currentFiles:
                    differences.append(i)

            for filename in differences:
                full_path = os.path.join(downloadsPath, filename)
                if os.path.exists(full_path):
                    zipFile(full_path, zipDir)

            inp = input("Show differences? [Y/N]: ")
            if inp.lower() == "y":
                print("Changed files:", differences)

            restore = input("Restore (unzip) all secured files back to "
                            "Downloads? [Y/N]: ")
            if restore.lower() == "y":
                for zfile in os.listdir(zipDir):
                    if zfile.endswith(".zip"):
                        unzipFile(os.path.join(zipDir, zfile), downloadsPath)

            x = input("Update downloads.txt with new file states? [Y/N]: ")
            if x.lower() == "y":
                saveDownloadsFilenames()

    except FileNotFoundError:
        print("[WARN] downloads.txt not found. Creating a new one.")
        saveDownloadsFilenames()
