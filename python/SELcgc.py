from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, date, timezone
import time

import json
import os

#import requests

def nLastLine(filename, n=1):
    #returns the nTH before the last line of a file (n=1 gives the last line)
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
        f.close()
    return last_line


def getStats():
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get("http://www.catgirl.io/farming")

    time.sleep(3)

    try:
        #elementp = WebDriverWait(driver, 5000).until(
        #        EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div/div[3]/div[2]/p/span[number(.) >= 3000000")))

        elementp = driver.find_element(By.XPATH,  "//*[@id='__next']/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div/div[3]/div[2]/p/span").text

        print(elementp.text)
    finally:
        element = driver.find_element(By.XPATH,  "//*[@id='__next']/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div/div[3]/div[2]/p/span").text
        poolSize = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div/div[2]/div[2]/p[1]/span").text
        cgcLock = driver.find_element(By.XPATH,  "//*[@id='__next']/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div/div[4]/div[2]/p[1]/span").text

        urlcgc = "https://api.pancakeswap.info/api/v2/tokens/0x79ebc9a2ce02277a4b5b3a768b1c0a4ed75bd936"
 #      // cgc = requests.request("GET", urlcgc).text
  #     // cgcJSON = json.loads(cgc)
   #    // if(cgcJSON["error"]):
    #   //     print(cgcJSON["error"])
        cgcPriceUSD = "0.000000000666"
        cgcPriceBNB = "0.00000000000111"
     #  // else:
      # //     cgcPriceUSD = cgcJSON["data"]["price"]
       #//     cgcPriceBNB = cgcJSON["data"]["price_BNB"]

        utime = int(time.time())

        driver.quit()

        print(poolSize)

        return Stats(poolSize, element, cgcLock, utime, cgcPriceUSD, cgcPriceBNB)

class Stats():
    def __init__(self, PS, TFP, CGL, Time, USD, BNB):
        self.time = Time
        self.poolSize = self.makeNum(PS)
        self.totalFP = self.makeNum(TFP)
        self.cgcLocked = self.makeNum(CGL)
        self.cgcPriceUSD = float(USD[0:17])
        self.cgcPriceBNB = float(BNB[0:17])
        self.bnbusd = 200
        self.lptokens = 30000
        self.bnblp = 666
        self.cgclp = 420000000000

    def makeNum(self, string):
        return int(float(string.replace(',','')))

tries = 0
dttime = datetime.now(timezone.utc)
print(dttime.strftime("%y%m%d-%H%M"))

stats = getStats()

while tries < 5 and stats.totalFP < 3000000:
    del stats
    stats = getStats()
    tries += 1

if tries < 5:
    SELcgc = open("../dat/cgclog.txt", "a")
    SELcgc.write(json.dumps(stats.__dict__))
    SELcgc.write('\n')
    SELcgc.close()

#Remove first line
    SELcgc = open("../dat/cgclog.txt", "r+")
    lines = SELcgc.readlines()
    SELcgc.seek(0)
    SELcgc.truncate()
    SELcgc.writelines(lines[1:])
    SELcgc.close()


    print(stats.cgcPriceUSD)

if tries >= 5:
    print("Could not scrape.")
    # Add functionality here to copy and append last entry to SELcgc.txt
    lastLine = nLastLine("../dat/cgclog.txt", 1)
    newLine = json.loads(lastLine)
    utime = int(time.time())
    newLine["time"] = utime
    lastLine = json.dumps(newLine)

    SELcgc = open("../dat/cgclog.txt", "a")
    SELcgc.write(lastLine)
    SELcgc.write('\n')
#Remove first line
    lines = SELcgc.readlines()
    SELcgc.seek(0)
    SELcgc.truncate()
    SELcgc.writelines(lines[1:])

    SELcgc.close()
