import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import quote_plus
import sys
from parseQuizContext import getContext, getQuizFormData, getQuestions, extractTextWithAnswer
import traceback


website = 'http://www.taiwantestcentral.com'
resource_folder = r'c:\resources'



def getHTML (url):

    if not os.path.exists(resource_folder):
        os.mkdir(resource_folder)
    
    html = ''

    cache_filename =  quote_plus(url[len(website):]) + '.html'
    if os.path.exists(os.path.join(resource_folder,cache_filename)):
        with open(os.path.join(resource_folder,cache_filename), encoding = 'utf-8') as f:
            html = f.read ()
    else:
        r = requests.get(url)

        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            #print (r.status_code)
            html = r.text
            fo = open(os.path.join(resource_folder,cache_filename), 'w', encoding = 'utf-8')
            fo.write (html)
            fo.close()

    return html

def outputError (filename, message):
    error_folder = os.path.join(resource_folder,'error')
    if not os.path.exists(error_folder):
        os.mkdir(error_folder)
    filename = quote_plus(filename[len(website):]) + '.error'
    fo = open(os.path.join(error_folder,filename), 'w', encoding = 'utf-8')
    fo.write (str(message))
    fo.close()


def parseWordList (path):            

    html = getHTML(website + path)

    myDict = {}

    if html != '':
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(html, 'html.parser')
        class_id = 'nowrap w1'
        if path.endswith('11'):
            class_id = 'nowrap w2'
            
        vocabularies = soup.find_all('td', class_=class_id)
        
        for vocab in vocabularies:
            # 新聞標題
            vocab_chi = vocab.findNextSibling("td", class_='Chinese')
            vocab_link_shell = vocab.findNextSibling("td", class_='Freq')
            vocab_link = vocab_link_shell.find("a")

            vocab_link_string = ''
            vocab_count = '0'
            if vocab_link == None:
                vocab_link_string = 'None'
            else:
                vocab_link_string =  vocab_link.get('href') 
                if vocab_link_string != None:
                    vocab_link_string = '/' + vocab_link_string
                vocab_count = vocab_link.string

            #print  (vocab.string)
            #print (vocab_link.string) 
            vocab_set =  {} 
            vocab_set["chi"] = vocab_chi.string
            vocab_set["link"] = vocab_link_string
            vocab_set["count"] = vocab_count

            myDict[vocab.string] =  vocab_set
            #print (vocab.string + ' ' + vocab_chi.string + ' ' + vocab_link_string + ' ' + vocab_count )
        
    return myDict        


def getQuizList (word):
    
    #path = '/wordlist/WordQuestions.aspx?MainCategoryID=2&Word=zoo'
    
    path = '/wordlist/WordQuestions.aspx?MainCategoryID=2&Word='+ word
    html = getHTML(website + path)
    
    quizzes = None
    # 確認是否下載成功
    if html != '':
    # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(html, 'html.parser')

        quizzes = soup.find_all('a', target='PopupQuestion')

        '''
        for quiz in quizzes:
            print (quiz.get('href'))
            print (quiz.string)
        '''

    return quizzes

def getQuizForm (url, wordListDict):
    formData =  []
    try:
        html = getHTML(website + url)
        if html != '':
            soup = BeautifulSoup(html, 'html.parser')

            formData =  []

            form = soup.find ('form')
            post_url = form.get("action")
            print ('action = ' + post_url)
            formData.append(post_url)

            inputs = form.find_all ('input')
            pairs = {}
            for input in inputs:
                #print  (input.get('name')+' = ' +input.get('value'))
                pairs[input.get('name')] = input.get('value')

            formData.append(pairs)
            ##### 上面是為了要拿答案，所以需要取得form post的參數，給下一階段使用

    except BaseException as err :
        print (err)
        print ('ERROR : ' + url , sys.exc_info()[0] )
        outputError(url,  sys.exc_info()[0])
        traceback.print_exc()


    return formData



def getQuizDetail (formData, wordSet):

    post_folder = os.path.join(resource_folder, 'post')
    if not os.path.exists(post_folder):
        os.mkdir(post_folder)
    
    url = website +'/Tests/'+ formData[0]

    html = ''
    cache_filename =  quote_plus(url[len(website):]) + '.html'
    if os.path.exists(os.path.join(post_folder,cache_filename)):
        with open(os.path.join(post_folder,cache_filename), encoding = 'utf-8') as f:
            html = f.read ()
    else:
        url = website +'/Tests/'+ formData[0]
        r = requests.post(url,data=formData[1])
        if r.status_code == requests.codes.ok:
            html = r.text
            fo = open(os.path.join(post_folder,cache_filename), 'w', encoding = 'utf-8')
            fo.write (html)
            fo.close()


def getQuizForm_And_Parse (url, wordSet):
    formData =  []
    ctx = {}
    try:
        html = getHTML(website + url)
        if html != '':
            soup = BeautifulSoup(html, 'html.parser')

            ##### 為了要拿答案，所以需要取得form post的參數，給下一階段使用
            formData =  getQuizFormData(soup)
          
            ### 下面是判斷如果是題組，題組的本文拉出來。  如果是單一題，把題目拉出來
        #isPopupGroup = url.find('PopupGroup') != -1  # 表示這是題組
        #if not isPopupGroup:
            html = html.replace ('&#x2003;','_')  # if it's single question (PopupQuestion), restore the html unicode character.

            soup = BeautifulSoup(html, 'html.parser')
            ctx = getContext(soup)

            ctx['url'] = url.replace ('/dummy/..','')
        
        # Handle Quiz Parsing
            quizzes = ctx.get('quiz')
            if quizzes == None:
                quizzes = list()
                ctx['quiz'] = quizzes
            
            getQuestions(soup, quizzes)
            #quizzes.append(quiz)

        # Handle Exam
            exam = wordSet.get('exam')
            if exam == None:
                exam = []
                wordSet['exam'] = exam
            exam.append(ctx)
    except BaseException as err :
        print (err)
        print ('ERROR : ' + url , sys.exc_info()[0] )
        outputError(url,  sys.exc_info()[0])
        traceback.print_exc()


    return formData, ctx




def getQuizDetail_And_Parse (formData, context):

    post_folder = os.path.join(resource_folder, 'post')
    if not os.path.exists(post_folder):
        os.mkdir(post_folder)
    
    url = website +'/Tests/'+ formData[0]

    html = ''
    cache_filename =  quote_plus(url[len(website):]) + '.html'
    if os.path.exists(os.path.join(post_folder,cache_filename)):
        with open(os.path.join(post_folder,cache_filename), encoding = 'utf-8') as f:
            html = f.read ()
    else:
        url = website +'/Tests/'+ formData[0]
        r = requests.post(url,data=formData[1])
        if r.status_code == requests.codes.ok:
            html = r.text
            fo = open(os.path.join(post_folder,cache_filename), 'w', encoding = 'utf-8')
            fo.write (html)
            fo.close()

    if html != '':
        soup = BeautifulSoup(html, 'html.parser')


        quiz = None
        quizzes = list()
        context['quiz_with_answer'] = quizzes
        tds = soup.find_all ('td', class_=['QuestionNumber','QuestionText','CorrectAnswer','Remark'])    # find each question and extract the text
        for td in tds:

            tag = td['class'][0]
            if tag == 'QuestionNumber':
                num = 'None'
                if td.string != None:
                    num = td.string.strip() 
                quiz = {}
                quiz['QuestionNumber'] = num
            elif tag == 'QuestionText':
                quiz = extractTextWithAnswer(td)       
            elif tag == 'CorrectAnswer':
                answer = 'None'
                if td.string != None:
                    answer = td.string.strip()
                quiz['answer'] = answer
                quizzes.append(quiz)
            elif tag == 'Remark':
                remark = 'None'
                if td.string != None:
                    remark = td.string.strip()
                if quiz == None:
                    context['remark'] = remark
                else:
                    quiz['remark'] = remark

        
   



            



        
"""
        vocab_chi = vocab.findNextSibling("td", class_='Chinese')
        vocab_link_shell = vocab.findNextSibling("td", class_='Freq')
        vocab_link = vocab_link_shell.find("a")

        vocab_link_string = ''
        vocab_count = '0'
        if vocab_link == None:
            vocab_link_string = 'None'
        else:
            vocab_link_string =  vocab_link.get('href') 
            vocab_count = vocab_link.string

        #print  (vocab.string)
        #print (vocab_link.string) 
        vocab_set =  {} 
        vocab_set["chi"] = vocab_chi.string
        vocab_set["link"] = vocab_link_string
        vocab_set["count"] = vocab_count
"""

#getQuizList ('zoo')

#ctx = getQuizForm ('http://www.taiwantestcentral.com/Tests/PopupGroup.aspx?ID=75&Highlight=visit')
#getQuizDetail (None)

