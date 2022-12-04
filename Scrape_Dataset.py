import streamlit as sl
import snscrape.modules.twitter as sntwitter
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
sl.set_page_config(
    page_title="Sentimen Analisis"
)

sl.sidebar.header('SKRTT Team \n`IT Project`  `Sentimen Anlisis`')


sl.title('Scrape Dataset')


#since dan untill untuk menentukan tanggal dimulainya dan tanggal terakhirnya pada tweet
since = str(sl.date_input('Since'))
until = str(sl.date_input('Until'))

#variable query berfungsi untuk memberikan parameter data yang akan diambil
query = "(ganjar OR anies) lang:id until:"+until+" since:"+since
tweets = []
#variable limit digunakan untuk memberikan jumlah maksimal untuk mengammbil data tweet
limit = int(sl.number_input('Sum of Data',value=0))



bScrape = sl.button('Scraping Tweet')
#function scrape bergfungsi untuk menjalankan scrapping tweet pada twitter
def scrape():
    if bScrape:
        sl.write("Mulai Scraping")
        sl.write("********")
        for tweet in sntwitter.TwitterSearchScraper(query=query).get_items():
            if len(tweets) == limit:
                break
            else:
                tweets.append([tweet.date, tweet.user.username, tweet.content])
        df = pd.DataFrame(tweets, columns=['date','username','content'])
        sl.write("Finished")
        sl.write("********")
        sl.write("Berhasil mengambil tweet sebanyak")
        sl.write(df.count(axis=0))
        
        sl.download_button('Download Dataset',df.to_csv(),mime = 'text/csv')
    else:
        pass 
scrape()