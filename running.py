from flask import Flask, render_template, request, session
from flask_session import Session

import nltk
import numpy as np
import random
import string #processing python strings
from sklearn.feature_extraction.text import TfidfVectorizer#used to find similarity btwn words entered by users and words in file
from sklearn.metrics.pairwise import cosine_similarity
import cgi, cgitb

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)



@app.route('/', methods=["GET", "POST"])
def indexing():
    if request.method == "GET":
        return render_template ('homepage.html')
    else:
        creditscore()
        return render_template('homepage.html')

def greeting(sentence):
    #greeting inputs
    greetingInputs = ("hello","hi","ssup","hey","what's up")
    greetingResponses = ["hi","hello","hi there","I am glad you are talking to me"]
    for word in sentence.split():
        if word.lower() in greetingInputs:
            return random.choice(greetingResponses)

#reading the data
@app.route('/creditscore', methods=["POST",])
def creditscore():
    user_text = request.form.get("user", "No request")

    f = open('creditscore.txt','r',errors ='ignore')
    fileContents = f.read()
    fileContents = fileContents.lower() #converting to lowercase
    emmaResponse = ''


    sentences = nltk.sent_tokenize(fileContents) #tokenizes sentences
    words = nltk.word_tokenize(fileContents) #tokenizes words
    # stopwords = nltk.corpus.stopwords.words('english')
    # a = ['ha','le','u','wa']
    # stopwords.append(a)

    lemmer = nltk.stem.WordNetLemmatizer()

    #takes input as tokens returns normalized tokens
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    removepunc = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(removepunc)))



    #generating responses
    def response(userResponse):
        emmaResponse = ''
        sentences.append(userResponse)
        TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words = None)
        tfidf = TfidfVec.fit_transform(sentences)
        vals = cosine_similarity(tfidf[-1], tfidf) #[-1] represents axis
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if(req_tfidf==0):
            emmaResponse = emmaResponse + "Sorry, I do not understand you.Try again"
            return emmaResponse
        else:
            emmaResponse = emmaResponse + sentences[idx]
            return emmaResponse

    #making the bot more conversational
    # flag = True
    response_to_send = """EMMA: Hello, my name is Emma.I am here to answer your questions about credit score and give you some
     advice on how to improve it.If you want to exit, type done"""
    userResponse = user_text
    userResponse = userResponse.lower()
    if(userResponse!='done'):
        if(userResponse == "thanks" or userResponse =='thank you' or userResponse == 'Asante' or userResponse =='Asante sana'):
            emmaResponse = "EMMA: You are welcome"
        else:
            if(greeting(userResponse) != None):
                emmaResponse = "EMMA: "+greeting(userResponse)
            elif(userResponse == "wamlambezz"):
                emmaResponse = "EMMA: Wamnyonyezz!!"
            else:
                emmaResponse = response(user_text)
    else:
        emmaResponse = "Have a good day"
            # print("Have a good day.Take care")
    session['chat_history'] =[] if session.get("chat_history", None) is None else (session['chat_history'])
    values = session['chat_history'].append({"you":user_text, "":emmaResponse})
    #session.clear()
    return emmaResponse

# x = creditscore()
if __name__ == "__main__":
    app.run(debug=True)
