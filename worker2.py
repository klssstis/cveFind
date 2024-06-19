import os

os.system('pip3 install pytesseract numpy matplotlib opencv-python pillow')
os.system('apt-get update&&apt-get install -y tesseract-ocr')
os.system('apt-get install -y git-restore-mtime')

import requests
import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import re
import json
import sys
import time


os.system('apt-get update')
os.system('apt-get install -y python3 python3-pip nano git cmake pkg-config')
os.system('apt-get install -y --no-install-recommends ruby-dev libssl-dev libicu-dev zlib1g-dev libcurl4-openssl-dev')

os.system('pip3 install ghlinguist')
os.system('gem install github-linguist')

from glob import glob
import json
import os
import ghlinguist as ghl

import datetime

try:
    bot_token = sys.argv[1]
    chats = []
    chats.append(str(sys.argv[2]))
    print(len(chats))
except IndexError:
    print("not all parameters")
    os._exit(0)

send_text = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
response = requests.get(send_text)

for i in response.json()['result']:
    if str(i['message']['chat']['id']) in chats:
        continue
    chats.append(str(i['message']['chat']['id']))


def telegram_bot_sendtext(bot_message,bot_token,listUsers):
    for i in listUsers:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + i + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)

def sendImage(bot_image,bot_token,listUsers):
    for i in listUsers:
        url = "https://api.telegram.org/bot"+ bot_token +"/sendPhoto";
        files = {'photo': open(bot_image, 'rb')}
        data = {'chat_id' : i}
        r= requests.post(url, files=files, data=data)

gitCvelist = '/tmp/cvelist/'
if os.path.exists(gitCvelist):
    os.system('rm -rf '+gitCvelist)
os.system('git clone https://github.com/CVEProject/cvelistV5.git '+gitCvelist)
os.system('cd '+gitCvelist+'&&git restore-mtime')
fileListHash = []
for r, d, f in os.walk(gitCvelist+'cves/'):
  for file in f:
    if file.endswith('.json'):
      fileListHash.append(os.path.join(r, file))

listWeek = []
listNew = []

for i in fileListHash:
#    print(i)
    motime = datetime.datetime.fromtimestamp(os.stat(i).st_mtime)
#    print(motime)
#    print(datetime.datetime.now()-motime)
    countDays = (datetime.datetime.now()-motime).days
    if  countDays > 7:
        continue
    elif countDays < 1:
        listNew.append(i)
    else:
        listWeek.append(i)

#main module
telegram_bot_sendtext('daily update CVE '+str(len(listNew)),bot_token,chats)
for i in listNew:
    with open(i) as f:
        try:
            dictJsonTmp = json.load(f)
        except:
            print('except')
            print(i)
            continue
    if 'containers' in dictJsonTmp and 'cna' in dictJsonTmp['containers'] and 'descriptions' in dictJsonTmp['containers']['cna'] and 'value' in dictJsonTmp['containers']['cna']['descriptions'][0]:
        if '** RESERVED ** This candidate has been reserved' in dictJsonTmp['containers']['cna']['descriptions'][0]['value']:
            continue
        if 'Cross-Site Scripting' in dictJsonTmp['containers']['cna']['descriptions'][0]['value']:
            continue
        if 'In the Linux kernel' in dictJsonTmp['containers']['cna']['descriptions'][0]['value']:
            continue
            
        telegram_bot_sendtext('https://nvd.nist.gov/vuln/detail/'+i.split('/')[-1].split('.json')[0]+'\n\n'+dictJsonTmp['containers']['cna']['descriptions'][0]['value'],bot_token,chats)
