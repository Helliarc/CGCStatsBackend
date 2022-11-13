import mysql.connector
import json
import os
from configparser import ConfigParser

configur = ConfigParser()
configur.read("../.creds/dbCreds.ini")
account = 'admin1'
mydb = mysql.connector.connect(
    host=configur.get(account,"host"),
    user=configur.get(account,"user"),
    password=configur.get(account,"password"),
    database=configur.get(account,"database")
)

#returns the last line of a file
def lastLine(filename):
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while num_newlines < 1:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
        f.close()
    return last_line

#insert the log to the DB
def insertLog(log):
    logcursor = mydb.cursor()

    stmt = "INSERT INTO stats (time, poolsize, fp, cgclock, usd, bnb, BNBUSD, LPTokens, BNBLP, CGCLP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals = (log["time"], log["poolSize"], log["totalFP"], log["cgcLocked"], log["cgcPriceUSD"], log["cgcPriceBNB"], log["bnbusd"], log["lptokens"], log["bnblp"], log["cgclp"])

    try:
        logcursor.execute(stmt, vals)

        mydb.commit()

    except:
        mydb.rollback()
        print("Error posting Data")

    print("Data Inserted!")

def pullLastLog():
    logcursor = mydb.cursor()
    stmt = "SELECT * FROM stats ORDER BY time DESC LIMIT 1"
    try:
        logcursor.execute(stmt)
        result = logcursor.fetchall()

        return result
    except:
        mydb.rollback()
        print("Error Pulling Data")

#get last entry from scrapeLog
lastLog = json.loads(lastLine('..\dat\cgclog.txt'))
print(lastLog)
insertLog(lastLog)
lastResult = pullLastLog()
print(lastResult)

if lastResult != None:
    file = open("../dat/current.txt", "w")
    json.dump(lastResult, file)
    file.close()

mydb.close()
