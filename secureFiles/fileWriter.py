import os
from datetime import datetime
def updateLog(reason):
    user = os.getlogin()
    now = str(datetime.now())
    log = str(reason) + " " + now
    try:
        theFile = open("C:/Users/" + user + "/Documents/Sentry/secureFiles/trustedLogs/logs.txt","x")
        theFile.write(log)
        print("Something deleted the logs. I had to re-make it, so please check your computer.")
        theFile.close()
    except FileExistsError:
        theFile = open("C:/Users/" + user + "/Documents/Sentry/secureFiles/trustedLogs/logs.txt","a")
        theFile.write(log + "\n")
        print("Download log updated (see 'Documents/Sentry/secureFiles/trustedLogs/logs.txt' to view)")
        theFile.close()

