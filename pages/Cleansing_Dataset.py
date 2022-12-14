import streamlit as sl
import pandas as pd
import time
import emoji
import contractions
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import googletrans
from googletrans import *
import matplotlib.pyplot as plt
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

  

sl.sidebar.header('SKRTT Team \n`IT Project`  `Sentimen Anlisis`')

sl.title('Clean')
uploaded_file = sl.file_uploader(label='Upload your dataset.',
            type=['csv','xlsx'])

if uploaded_file is not None:
    print(uploaded_file)
    print('hello')
    
    try:
        df2 = pd.read_csv(uploaded_file)
        sl.write(df2)    
                
        
    except Exception as e:
        print(e)
        df2 = pd.read_excel(uploaded_file)
    
    else:
        def clean(tweet):
            #Replace RT
            t1 = re.sub('RT\s', '', tweet)
            #Replace @
            t2 = re.sub('\B@\w+', '', t1)
            #Replace Emoji
            t3 = emoji.demojize(t2)
            #Replace URL
            t4 = re.sub('(http|https):\/\/\S+','',t3)
            #Replace Hastag
            t5 = re.sub('#+', '', t4)
            #all lower
            t6 = t5.lower()
            #Replace repetition word
            t7 = re.sub(r'(.)\1+', r'\1\1', t6)
            #replace symbol repetition
            t8 = re.sub(r'[\?\.\!]+(?=[\?.\!])','',t7)
            #Alphabaet, del number and symbols
            t9  =re.sub(r'[^a-zA-Z]', ' ', t8)
            #replace contractions
            t10 = contractions.fix(t9)
            return t9

        for i, r in df2.iterrows():
            y = clean(r['content'])
            df2.loc[i,'content'] = y

        sl.title('Cleansing Data')
        sClean = sl.button('Show Clean Data')
        if sClean:
            sl.write(df2.head())


        #variable translator berfungsi untuk mentranslate kolom tweet yang masih berbahasa indonesia menjadi bahasa inggris
        translator = googletrans.Translator()

        df2['content'] = df2['content'].astype(str) #changing datatype to string
        df2['trans_content'] = df2['content'].apply(translator.translate, src='id', dest='en').apply(getattr, args=('text',))

        sl.title('Translate Data')
        #varibale dibawah untuk menampilkan data yang berhasil di translate
        sTrans = sl.button('Show Translate Data')
        if sTrans:
            sl.write(df2.head())
            
        #variable dibawah berfungsi untuk memberikan label tiap perkata
        pos_dict = {'J':wordnet.ADJ,'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

        #function dibawah adalah lanjutan variable diatas yaitu memberi label tiap perkata bahasa inggris
        def token_stop_pos(text):
            tags = pos_tag(word_tokenize(text))
            newlist = []
            for word, tag in tags:
                if word.lower() not in set(stopwords.words('english')):
                    newlist.append(tuple([word, pos_dict.get(tag[0])]))
            return newlist

        df2['tokenize'] = df2['trans_content'].apply(token_stop_pos)
        sl.title('Tokenie')    
        sl.write(df2.head())

        wordnet_lemmatizer = WordNetLemmatizer()

        #fuction dibawah berfungsi untuk menggabungkan kata yang sudah di pisah pisah menjadi satu kalimat/paragraf dengan kata yang baku
        def lemmatize(pos_data):
            lemma_r = " "
            for word, pos in pos_data:
                if not pos:
                    lemma = word
                    lemmar_r = lemma_r + " " + lemma
                else:
                    lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
                    lemma_r = lemma_r + " " + lemma
            return lemma_r
        df2['Lemma']=df2['tokenize'].apply(lemmatize)

        sl.title('Lemmatie')    
        sl.write(df2.head())
        sl.download_button('Download Dataset',df2.to_csv(),mime = 'text/csv')        


