import PyPDF2
import textract
import spacy
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
import os
import glob
import pdfkit
from docx2pdf import convert
import textract
from win32api import GetShortPathName
import pandas as pd
import requests 
import json
import ast
import re
from pandas.core.frame import DataFrame 
import tweepy 
import nltk
import pandas as pd
import numpy as np
import seaborn as sns
import spacy
import string
import collections
import matplotlib.pyplot as plt
import en_core_web_sm
from wordcloud import WordCloud,STOPWORDS
nltk.download('punkt')   
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from tweepy import OAuthHandler 
from textblob import TextBlob
from bs4 import BeautifulSoup
from string import punctuation
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score





nlp = en_core_web_sm.load() 
tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
stop = set(stopwords.words('english'))
punctuation = list(string.punctuation) #already taken care of with the cleaning function.
stop.update(punctuation)
w_tokenizer = WhitespaceTokenizer()




def preprocess_text(text):
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.lower() not in stop_words]
    
    # Remove punctuation and URLs
    words = [re.sub(r'[^\w\s]', '', word) for word in words]
    words = [re.sub(r'http\S+', '', word) for word in words]
    
    # Tokenization
    tokens = word_tokenize(" ".join(words))
    
    # Stemming
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in tokens]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
    
    return lemmatized_words

def textextr(files):
    for file in files:
        print(f"******{file}*******")
        if file.lower().endswith(".doc"):
            continue
        text = textract.process(file)
        text = text.decode('utf-8')
        dataclean(text)
        #print(text)
        #print("==========================")


def dataclean(text):
    text = re.sub(r'&[^;]+;', '', text)
    text = re.sub(r'[^\x20-\x7F\n]+','',text)
    # text = re.sub(r'\s+', ' ', text)
    # text = re.sub(r'[ \t]+', '', text)
    text = re.sub(r'\t+','',text)
    # text = re.sub(r'\n+','',text)
    text = re.sub('Page [0-9] of [0-9]', '', text)
    text = re.sub("(?i)resume", "", text)
    text = re.sub("\n", " ", text)

    # print(text)
    words = text.split('\n')
    textpostnlp = preprocess_text(text)
    print("***********************************\n")
    print(textpostnlp)
    print("***********************************\n")
    words = [string for string in words if string != ""]
    # print(text)
    print(f"*********\n{words}\n*********\n")
    tempemail = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',text) 
    tempemail = "" if tempemail is None else tempemail.group(0)
    tempnum = re.findall( r'\+?\d{1,2}[-\s]*\d{3}[-\s]*\d{1}[-\s]*\d{1}[-\s]*\d{1}[-\s]*\d{1}[-\s]*\d{1}[-\s]*\d{1}[-\s]*\d{1}', text)
    # tempnum = re.sub(r'[-\s]', '', tempnum)
    tempnum = [number.replace(" ", "").replace("-","")[-10:] for number in tempnum]
    score = jobmapping(corpus,textpostnlp)
    print(score)
    datasetprof.append((words[0],tempemail,tempnum[0],text,textpostnlp,score))



def jobmapping(corpus,text):
    intersection = set(text).intersection(set(corpus))
    union = set(text).union(set(corpus))
    return len(intersection)/len(union)
    

datasetprof=[]
path = 'data'


files = glob.glob(os.path.join(path, '*.*'))
corpus = preprocess_text("Functional consultants play a critical role in implementing technology solutions to meet the specific business needs of a client. Some of the technical skills that a functional consultant should possess include: Knowledge of business processes: A functional consultant should have a deep understanding of the business processes they are working with, including finance, supply chain management, human resources, etc Technical knowledge of software systems: A functional consultant should be well-versed in the software systems they are implementing, including their architecture, data models, and functionalities Project management: Functional consultants should have experience in project management, including planning, execution, and delivery of projects within deadlines Problem-solving: A functional consultant should be able to diagnose and solve technical problems related to the software systems they are working with Communication: Effective communication is critical for functional consultants, who must be able to articulate technical concepts to both technical and non-technical stakeholders Data analysis: Functional consultants should be able to analyze data, identify trends and insights, and use them to drive business decisions Technical writing: Functional consultants should have strong writing skills to document functional requirements, user manuals, and training materials Adaptability: Technology is constantly changing, and functional consultants should be able to adapt to new technologies and systems quickly.")
textextr(files)
print(datasetprof)
datasetprofdf = pd.DataFrame(datasetprof,columns=['Name','Email','Phone Number','Text','Job Corpus','Similarity Score'])
datasetprofdf.sort_values("Similarity Score", ascending=False, inplace=True)
datasetprofdf.to_csv('datasetprof.csv',index=False)

