#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import flask
from flask import Flask,jsonify,request
import re
import nltk
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')


app=Flask(__name__)

@app.route("/summary/",methods=['POST','GET'])
def return_summary():
    #article_text='Either you love it or hate it, but in the age of Microservice and REST API, you can not ignore JavaScript. JavaScript was once upon a time used only in client side(browser), but node js (execution engine/run time/web server) have made possible to run javascript on server side. JavaScript is everywhere – on Desktop/Server/Mobile.You can create mobile web app with javascript and html5, which has lot of advantages like save licensing cost $99 yearly to pay Apple for making IOS apps and you don’t have to purchase MAC laptop to make your IOS app(Apple’s app can only be made in MAC). JavaScript has stormed the web technology and nowadays small software ventures to fortune 500, all are using node js for web apps. Recently wordpress.com has rewritten its dashboard in javascript, paypal also chose to rewrite some of its components in java script. Be it google/twitter/facebook, javascript is important for everyone. It is used in applications like single page applications, Geolocation APIs, net advertisements etc. However JavaScript is quirky/dynamic/scripting/ functional oriented language, and it has its own idiosyncrasies. It is not scalable, it is good for some 3000 line of code but for a bigger app, it becomes difficult to manage ,read and debug. Also not everyone is very much familiar to JavaScript.'
    page = requests.get("https://www.arcesb.com/resources/edi/")
    soup = BeautifulSoup(page.content, 'html.parser')
    text=""
    for i in soup.find_all('p'):
        text+=i.get_text()
    #article_text=request.args.get('document')
    
    article_text=text
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    #formatted_article_text=article_text
    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    #summary_sentences = heapq.nlargest(4, sentence_scores, key=sentence_scores.get)
    summary_sentences= sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary_sentences =summary_sentences[0:4]
    #summary = ' '.join(summary_sentences)
    ordered_summary=''
    '''
    for sentence in sentence_list:
        if(sentence in summary_sentences):
            ordered_summary+=sentence
'''
    for i in sentence_scores:
        ordered_summary+=i
    return jsonify({'summary':ordered_summary})
    



@app.route("/",methods=['GET'])
def default():
    return "<h1> Welcome <h1>"

if __name__=="__main__":
    app.run()


# In[ ]:




