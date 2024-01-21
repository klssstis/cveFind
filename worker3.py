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


os.system('sudo apt-get update')
os.system('sudo apt-get install -y python3 python3-pip nano git cmake pkg-config')
os.system('sudo apt-get install -y --no-install-recommends ruby-dev libssl-dev libicu-dev zlib1g-dev libcurl4-openssl-dev')

os.system('sudo pip3 install ghlinguist')
os.system('sudo gem install github-linguist')

from glob import glob
import json
import os
import ghlinguist as ghl

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
    if i['message']['chat']['id'] in chats:
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
os.system('git clone https://github.com/CVEProject/cvelist.git '+gitCvelist)
os.system('cd '+gitCvelist+'&&git restore-mtime')
fileListHash = []
for r, d, f in os.walk(gitCvelist):
  for file in f:
    if file.endswith('.json'):
      fileListHash.append(os.path.join(r, file))


#main module

telegram_bot_sendtext('daily top EPSS',bot_token,chats)

img_data = requests.get('https://www.first.org/epss/figures/top_cve_last_30_days-1.png').content
with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)
image = cv2.imread("image_name.jpg")
string = pytesseract.image_to_string(image)

sendImage("image_name.jpg",bot_token,chats)

listCVE=[]
for i in re.split('\n| |CVE|CWE',string):
    if i.startswith('-') and len(re.findall('-',i))==2:
      listCVE.append('CVE'+i)
st = ''
for i in sorted(listCVE):
    st+=i+','

for i in fileListHash:
    if i.split('/')[-1].split('.json')[0] in listCVE:
      with open(i) as f:
        try:
            dictJsonTmp = json.load(f)
        except:
            print(i)
            continue
        if 'description' in dictJsonTmp and 'description_data' in dictJsonTmp['description'] and 'value' in dictJsonTmp['description']['description_data'][0]:
            telegram_bot_sendtext('https://nvd.nist.gov/vuln/detail/'+i.split('/')[-1].split('.json')[0],bot_token,chats)
            telegram_bot_sendtext(dictJsonTmp['description']['description_data'][0]['value'],bot_token,chats)
