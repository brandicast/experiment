import  taiwan_test_central_tools  as ttc
import time
import random
import os
import json
import threading

#import hashlib
#from urllib.parse import urlencode, urlparse, quote_plus

website = 'http://www.taiwantestcentral.com'
ResourceFolder = ttc.resource_folder
CachedJsonFile = os.path.join(ResourceFolder,'ttc.json')

MAX_WORKER = 3
WORKER = 3
AVAILABLE_WORKER = True

def doJob (args, lock, wordSet):
    global WORKER
    lock.acquire()
    WORKER -= 1
    lock.release()
    print (time.asctime( time.localtime(time.time()) ) + ' Thread number : ' + str(WORKER) + ' Thread id : ' + str(threading.current_thread().ident) + ' start !' ) 
    formData = ttc.getQuizForm(args, wordSet)
    time.sleep(random.randrange(3,5))
    print (time.asctime( time.localtime(time.time()) ) + ' Thread number : ' + str(WORKER) + ' Thread id : ' + str(threading.current_thread().ident) + ' finish getting form and ready to get detail' ) 
    ttc.getQuizDetail (formData, wordSet)
    lock.acquire()
    WORKER += 1
    lock.release()
    print (time.asctime( time.localtime(time.time()) ) + ' Thread number : ' + str(WORKER) + ' Thread id : ' + str(threading.current_thread().ident) + ' finish getting detail' ) 



##### Main start here
wordList = None
if not os.path.exists(CachedJsonFile):
    wordList = ttc.parseWordList()
    json.dump(wordList,open(CachedJsonFile,'w',encoding = 'utf-8'),ensure_ascii=False)
    
else:
    print ('Load from cache file:' + CachedJsonFile)
    wordList = json.load(open(CachedJsonFile, encoding = 'utf-8'))

counter = 0
START = False
for word in wordList.keys():
    if word == 'with':
        START = True
    
    if START:
#    print (time.asctime( time.localtime(time.time()) ) + ' Downloading........' + word, end='')
        quizzes = ttc.getQuizList(word)
    
        lock = threading.Lock()
        while (AVAILABLE_WORKER and quizzes):
        
            if WORKER >0 and WORKER<=MAX_WORKER :
                quiz = quizzes.pop()
                t = threading.Thread (target = doJob, args = ('/dummy/' + quiz.get('href'),lock,wordList[word],))
                t.start()
            else:
                time.sleep(3)
            AVAILABLE_WORKER = (WORKER <=MAX_WORKER)



    


'''
website = 'http://www.taiwantestcentral.com'

#ttc.getWordList(website + '/wordlist/BCTWordList.aspx?CategoryID=12')



s = '/wordlist/BCTWordList.aspx?CategoryID=12'

hash_object = hashlib.sha256(s.encode('utf-8'))
hex_dig = hash_object.hexdigest()
print(hex_dig)


url = website + s
url = 'http://www.taiwantestcentral.com/Tests/PopupGroup.aspx?ID=75&Highlight=visit'

cache = url[len(website):]

print (cache)
print (quote_plus(cache))
print (urlparse(website + s).netloc)
print (urlparse(website + s).query)
'''