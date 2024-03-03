import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import quote_plus
import sys
import taiwan_test_central_tools as ttc

website = 'http://www.taiwantestcentral.com'
ResourceFolder = ttc.resource_folder
CachedJsonFile = os.path.join(ResourceFolder,'ttc.json')

wordList = None

if not os.path.exists(CachedJsonFile):
    #path = '/wordlist/BCTWordList.aspx?CategoryID=12'  # 1200 words
    path = '/wordlist/BCTWordList.aspx?CategoryID=11'  # 800 words
    wordList = ttc.parseWordList(path)
    json.dump(wordList,open(CachedJsonFile,'w',encoding = 'utf-8'),ensure_ascii=False)
    
else:
    print ('Load from cache file:' + CachedJsonFile)
    wordList = json.load(open(CachedJsonFile, encoding = 'utf-8'))


#url='/dummy/../Tests/PopupGroup.aspx?ID=23&Highlight=air'   # text only
#url='/dummy/../Tests/PopupGroup.aspx?ID=236&Highlight=enjoy' # image only
#url='/dummy/../Tests/PopupGroup.aspx?ID=1442&Highlight=enjoy' # text with span
url = '/dummy/../Tests/PopupGroup.aspx?ID=218&Highlight=usual' # weird
#url='/dummy/../Tests/PopupQuestion.aspx?ID=517&Highlight=air'

ttc.getQuizForm_And_Parse(url,wordList['usual'])


'''
print ('checking', end='')
for file in os.listdir(r'C:\resources'):
    if file.find('PopupQuestion') != -1:
        sys.stdout.flush()
        try:
            getContext(file)
        except:
            print (file)
'''