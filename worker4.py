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

strStat = 'CVE language statistical-day \n\n'
for filename in listNew:
    try:
        with open(filename) as f:
            d = json.load(f)
            if 'references' in d.keys():
                for i in d['references']['reference_data']:
                    gitUrl = ''
                    if i['url'].startswith('https://github.com/'):
                        checkVal = len(i['url'].split('/'))
                        if checkVal<5:
                            print('not set repo '+','+d['CVE_data_meta']['ID']+','+i['url'])
                            print('\n')
                            continue
                        elif checkVal == 5:
                            gitUrl = i['url']
                        elif i['url'].split('/')[5] in ['issues','pull','releases','commit','compare']:
                            gitUrl = i['url'].split('/'+i['url'].split('/')[5])[0]
                        if gitUrl == '':
                            continue
                        os.system('rm -rf /tmp/123_1')
                        os.system('git clone '+gitUrl+' /tmp/123_1')
                        if not os.path.exists('/tmp/123_1'):
                            print('null repo '+','+d['CVE_data_meta']['ID']+','+gitUrl)
                            print('\n')
                            continue
                        langs = ghl.linguist('/tmp/123_1')
                        langStr = ''
                        for ln in langs:
                            if float(ln[1])>30:
                                langStr +=ln[0]+' '
                        strStat += langStr+','+d['CVE_data_meta']['ID']+','+gitUrl
                        strStat += '\n'
                    elif i['url'].startswith('https://gitlab.com/'):
                        checkVal = len(i['url'].split('/'))
                        if checkVal<5:
                            print('not set repo '+','+d['CVE_data_meta']['ID']+','+i['url'])
                            print('\n')
                            continue
                        elif checkVal == 5:
                            gitUrl = i['url']
                        elif i['url'].split('/')[5]+'/'+i['url'].split('/')[6] in ['-/merge_requests','-/commit/','-/issues/']:
                            gitUrl = i['url'].split('/-/')[0]
                        if gitUrl == '':
                            continue
                        os.system('rm -rf /tmp/123_2')
                        os.system('git clone '+gitUrl+' /tmp/123_2')
                        if not os.path.exists('/tmp/123_2'):
                            print('null repo '+','+d['CVE_data_meta']['ID']+','+gitUrl)
                            print('\n')
                            continue
                        langs = ghl.linguist('/tmp/123_2')
                        langStr = ''
                        for ln in langs:
                            if float(ln[1])>30:
                                langStr +=ln[0]+' '
                        strStat += langStr+','+d['CVE_data_meta']['ID']+','+gitUrl
                        strStat += '\n'
                    elif i['url'].startswith('https://git.'):
                        checkVal = len(i['url'].split('/'))
                        if checkVal<3:
                            print('not set repo '+','+d['CVE_data_meta']['ID']+','+i['url'])
                            print('\n')
                            continue
                        elif '?p=' in i['url'] and '.git;' in i['url']:
                            prjUrl = i['url'].split('?p=')[1].split(';')[0]
                            gitUrl = i['url'].split('/')[2]
                        if gitUrl == '':
                            continue
                        os.system('rm -rf /tmp/123_3')
                        os.system('git clone https://'+gitUrl+'/git/'+prjUrl+' /tmp/123_3')
                        if not os.path.exists('/tmp/123_3'):
                            os.system('git clone git://'+gitUrl+'/git/'+prjUrl+' /tmp/123_3')
                            if not os.path.exists('/tmp/123_3'):
                                os.system('git clone https://'+gitUrl+'/'+prjUrl+' /tmp/123_3')
                                if not os.path.exists('/tmp/123_3'):
                                    os.system('git clone git://'+gitUrl+'/'+prjUrl+' /tmp/123_3')
                        if not os.path.exists('/tmp/123_3'):
                            print('null repo '+','+d['CVE_data_meta']['ID']+','+gitUrl)
                            print('\n')
                            continue
                        langs = ghl.linguist('/tmp/123_3')
                        langStr = ''
                        for ln in langs:
                            if float(ln[1])>30:
                                langStr +=ln[0]+' '
                        strStat += langStr+','+d['CVE_data_meta']['ID']+','+gitUrl
                        strStat += '\n'

    except:
        print('except'+','+filename+','+filename)
        print('\n')
telegram_bot_sendtext(strStat,bot_token,chats)
