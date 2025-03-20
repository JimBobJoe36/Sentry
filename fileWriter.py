import os
from datetime import datetime
def updateLog():
    user = os.getlogin()
    print(user)

    now = str(datetime.now())
    print(now)
    try:
        theFile = open("C:/Users/" + user + "/Documents/Sentry/Secure Files/trustedLogs/logs.txt","x")
        theFile.write(now)
        print("Surprise!!!")
        theFile.close()
    except FileExistsError:
        theFile = open("C:/Users/" + user + "/Documents/Sentry/Secure Files/trustedLogs/logs.txt","a")
        theFile.write(now + "\n")
        print("Surprise!!!")
        theFile.close()