import mysql.connector
import json
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

def query(files,stmt):
    logcursor = mydb.cursor()
    
    
    try:
        logcursor.execute(stmt)
        result = logcursor.fetchall()
        if result != None:
            file = open(f'../dat/{files}.txt', 'w')
            json.dump(result, file)
            file.close()

    except:
        mydb.rollback()
        print("Error Pulling Data")


cgcusdSTMT = "SELECT DISTINCT minute(FROM_UNIXTIME(time)),time,usd FROM `stats` where minute(FROM_UNIXTIME(time)) = 00;"
cgcbnbSTMT = "SELECT DISTINCT minute(FROM_UNIXTIME(time)),time,bnb FROM `stats` where minute(FROM_UNIXTIME(time)) = 00;"
cgclockSTMT =  "SELECT DISTINCT minute(FROM_UNIXTIME(time)),time,cgclock FROM `stats` where minute(FROM_UNIXTIME(time)) = 00;"
poolsizeSTMT =  "SELECT DISTINCT minute(FROM_UNIXTIME(time)),time,poolsize FROM `stats` where minute(FROM_UNIXTIME(time)) = 00;"
cgcfpSTMT =  "SELECT DISTINCT minute(FROM_UNIXTIME(time)),time,fp FROM `stats` where minute(FROM_UNIXTIME(time)) = 00;"

chartNames = {'hourCGCUSD': cgcusdSTMT, 'hourCGCBNB': cgcbnbSTMT, 'hourCGCLock': cgclockSTMT, 'hourS1PoolSize': poolsizeSTMT, 'hourTotalFP': cgcfpSTMT}

for chart in chartNames:
    query(chart, chartNames[chart])
