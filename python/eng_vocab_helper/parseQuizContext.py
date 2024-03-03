import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import quote_plus
import sys


def extractText (tag):
    txt = ''
    for tmp in tag.find_all(text=True):     
        x = tmp.string.strip()
        if  len(x) > 0:
            if x == ',' or x == '?':
                txt += x
            else:
                txt +=  ' ' + x 
    txt = txt.strip()
    #print (txt)
    return txt

def extractTextWithAnswer (td_tag):
    quiz = {}
    div = td_tag.find ('div')     
    question = ''
    for tmp in div.find_all(text=True):     
        x = tmp.string.strip()
        if  len(x) > 0:
            if x == ',' or x == '?':
                question += x
            else:
                question +=  ' ' + x 
    question = question.strip()
    quiz['question'] = question

    answer_list = td_tag.find_all ('td', class_='AnswerRadio')
    options_array = []
    for answer in answer_list:
        answer_shell = answer.findNextSibling('td')
        option = ''
        for tmp in answer_shell.find_all(text=True):
            x = tmp.string.strip()
            if  len(x) > 0:
                if x == ',' or x == '?':
                    option += x
                else:
                    option +=  ' ' + x 
        options_array.append (option)  
    quiz['options'] = options_array
    return quiz

# this is to handle  --> <span class="SeqPlaceholder">1</span>
def extractContext (tag):
    txt = ''
    for tmp in tag.find_all():     
        if tmp.string != None:
            x = tmp.string.strip()

            isSepPlaceholder = False
            if tmp.get('class') != None:
                 isSepPlaceholder = tmp.get('class') [0] == 'SeqPlaceholder'

            if isSepPlaceholder:
                x = '___' + x + '___'
            if  len(x) > 0:
                if x == ',' or x == '?':
                    txt += x
                else:
                    txt +=  ' ' + x 
    txt = txt.strip()
    #print (txt)
    return txt


def getContext (soup):

    #questions = soup.find_all ('td', class_='QuestionNumber')   # 看看QuestionNumber有幾個，有多個表示是題組。 但後來發現其實可以用url區分
    #question_number = len(questions)
    #print ('Count = ',question_number)
    ctx = {}
    # 題組分兩種，一種是圖，一種是文字。To be Verified.  2021/09/16 馬上發現有 Hybrid --> 增加json欄位，有圖取圖，有字取字。  另外得處理  <span class="SeqPlaceholder">1</span> 
    group_picture = soup.find(id='TestQuestionRepeater_TestQuestion_0_GroupPicture_0')  # check if question context is only an image  *** need to verify if this could be 1) multiple pictures or 2) image and text mixed
    if group_picture != None:    # meaning this is an image question context           
        ctx['context_image'] = '/Tests/' + group_picture.get('src')   # this is already the image tag

    # 找文字題
    group_header = soup.find(id='TestQuestionRepeater_TestQuestion_0_GroupHeaderDiv_0')  
    if group_header != None:
        ctx['context'] = extractContext(group_header)

    return ctx


def getQuestions (soup, quizzes):
    quiz = None
    tds = soup.find_all ('td', class_=['QuestionNumber','QuestionText'])    # find each question and extract the text
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
            quizzes.append(quiz)
        
    #return quiz




def getQuizFormData (soup):
    formData = []
    form = soup.find ('form')
    post_url = form.get("action")
    formData.append(post_url)

    inputs = form.find_all ('input')
    pairs = {}
    for input in inputs:
        #print  (input.get('name')+' = ' +input.get('value'))
        pairs[input.get('name')] = input.get('value')

    formData.append(pairs)

    return formData