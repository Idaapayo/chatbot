import nltk
import numpy as np
import random
import string #processing python strings
from sklearn.feature_extraction.text import TfidfVectorizer#used to find similarity btwn words entered by users and words in file
from sklearn.metrics.pairwise import cosine_similarity
import cgi, cgitb

form = cgi.FieldStorage()
userResponse = form.getvalue('user')


#reading the data
def index():
    f = open('creditscore.txt','r',errors ='ignore')
    fileContents = f.read()
    fileContents = fileContents.lower() #converting to lowercase
    emmaResponse = ''


    sentences = nltk.sent_tokenize(fileContents) #tokenizes sentences
    words = nltk.word_tokenize(fileContents) #tokenizes words
    stopwords = nltk.corpus.stopwords.words('english')
    a = ['ha','le','u','wa']
    stopwords.append(a)

    lemmer = nltk.stem.WordNetLemmatizer()

    #takes input as tokens returns normalized tokens
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    removepunc = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(removepunc)))

    #greeting inputs
    greetingInputs = ("hello","hi","ssup","hey","what's up")
    greetingResponses = ["hi","hello","hi there","I am glad you are talking to me"]


    def greeting(sentence):
        for word in sentence.split():
            if word.lower() in greetingInputs:
                return random.choice(greetingResponses)

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
    flag = True
    print('EMMA: Hello, my name is Emma.I am here to answer your questions about credit score and give you some advice on how to improve it.If you want to exit, type done')

    while (flag==True):
        userResponse = input()
        userResponse = userResponse.lower()
        if(userResponse!='done'):
            if(userResponse == "thanks" or userResponse =='thank you' or userResponse == 'Asante' or userResponse =='Asante sana'):
                flag = False
                print("EMMA: You are welcome")
            else:
                if(greeting(userResponse) != None):
                    print("EMMA: "+greeting(userResponse))
                elif(userResponse == "wamlambezz"):
                    print("EMMA: Wamnyonyezz!!")
                else:
                    print("EMMA: ",end = "")
                    print(response(userResponse))
                    sentences.remove(userResponse)
        else:
            flag = False
            print("Have a good day.Take care")
    return index
                
x = index()                
            
          
        
        

