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

TARGET = 800

MAX_WORKER = 20
WORKER = 0
AVAILABLE_WORKER = True

ONLINE_MODE = False

def doJob (args, lock, wordSet):
    global WORKER
    lock.acquire()
    WORKER += 1
    lock.release()
    print ('Processing......', args)
    #print (time.asctime( time.localtime(time.time()) ) + ' Thread number : ' + str(WORKER) + ' Thread id : ' + str(threading.current_thread().ident) + ' start !' ) 
    vals = ttc.getQuizForm_And_Parse(args, wordSet)
    if ONLINE_MODE:
        time.sleep(random.randrange(3,5))
    #print (time.asctime( time.localtime(time.time()) ) + ' Thread number : ' + str(WORKER) + ' Thread id : ' + str(threading.current_thread().ident) + ' finish getting form and ready to get detail' ) 
    ttc.getQuizDetail_And_Parse (vals[0], vals[1])
    lock.acquire()
    WORKER -= 1
    lock.release()
    #print (time.asctime( time.localtime(time.time()) ) + ' Thread number : ' + str(WORKER) + ' Thread id : ' + str(threading.current_thread().ident) + ' finish getting detail' ) 

def persistentJson ():
    global wordList, START
    if (START):
        #print ('########################################Start#########################################')
        #print (wordList)
        #dumpJsonFile = os.path.join(ResourceFolder,'ttc_1200.json')
        if TARGET == 800:
            dumpJsonFile = 'ttc_800.json'
        else:
            dumpJsonFile = 'ttc_1200.json'
        json.dump(wordList,open(dumpJsonFile,'w',encoding = 'utf-8'),ensure_ascii=False)
        print ('Persistent Json File......')
        #print ('########################################End#########################################')
        #time.sleep(5)


##### Main start here

wordList = None

if not os.path.exists(CachedJsonFile):
    if TARGET == 800:
        path = '/wordlist/BCTWordList.aspx?CategoryID=11'  # 800 words
    else:
        path = '/wordlist/BCTWordList.aspx?CategoryID=12'  # 1200 words
    wordList = ttc.parseWordList(path)
    json.dump(wordList,open(CachedJsonFile,'w',encoding = 'utf-8'),ensure_ascii=False)
    
else:
    print ('Load from cache file:' + CachedJsonFile)
    wordList = json.load(open(CachedJsonFile, encoding = 'utf-8'))

counter = 0
START = True

for word in wordList.keys():
    '''
    if word == 'a':
        START = True
    else:
        START = False
    ''' 
    
    if START:
#    print (time.asctime( time.localtime(time.time()) ) + ' Downloading........' + word, end='')
        quizzes = ttc.getQuizList(word)
    
        lock = threading.Lock()
        while (AVAILABLE_WORKER and quizzes and START):
        
            if WORKER<=MAX_WORKER :
                quiz = quizzes.pop()
                t = threading.Thread (target = doJob, args = ('/dummy/' + quiz.get('href'),lock,wordList[word],))
                t.start()
                counter += 1
            elif ONLINE_MODE:
                time.sleep(5)
            
            '''
            if (counter % 20) == 0:
                print ('Counter = ' , counter)
                persistentJson()
            '''
            print ('Worker = ', WORKER)
            AVAILABLE_WORKER = (WORKER <=MAX_WORKER)
persistentJson()
        

    

