import os
from datetime import datetime
def updateLog():
    user = os.getlogin()
    now = str(datetime.now())
    print(now)
    try:
        theFile = open("C:/Users/" + user + "/Documents/Sentry/Secure Files/trustedLogs/logs.txt","x")
        theFile.write(now)
        print("Something deleted the logs. I had to re-make it, so please check your computer.")
        theFile.close()
    except FileExistsError:
        theFile = open("C:/Users/" + user + "/Documents/Sentry/Secure Files/trustedLogs/logs.txt","a")
        theFile.write(now + "\n")
        print("Download log updated (see 'Documents/Sentry/SecureFiles/trustedLogs/logs.txt' to view)")
        theFile.close()

