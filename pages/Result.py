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
from datetime import datetime
import datetime
from datetime import date

sl.sidebar.header('SKRTT Team \n`IT Project`  `Sentimen Anlisis`')

sl.title('Result')
uploaded_file = sl.file_uploader(label='Upload your dataset.',
            type=['csv','xlsx'])

if uploaded_file is not None:
    print(uploaded_file)
    
    try:
        df2 = pd.read_csv(uploaded_file)
        
        sl.write(df2)    

        def contain_candidate(tweet, candidate):
            if candidate == 'ganjar':
                if any(person in tweet.lower().replace(' ', '') \
                    for person in ['ganjar', 'pranowo']):
                    return 1
                else:
                    return 0
            elif candidate == 'anies':
                if any(person in tweet.lower().replace(' ', '') \
                    for person in ['anies', 'baswedan']):
                    return 1
                else:
                    return 0

        df2['ganjar'] = df2.content.apply(contain_candidate, args=('ganjar',))
        df2['anies'] = df2.content.apply(contain_candidate, args=('anies',))

        df2[['ganjar','anies']].sum()

        #memberi subject pada tiap sample
        def getSubjectivy(review):
            return TextBlob(review).sentiment.subjectivity

        #Memberi polarity pada tiap sample
        def getPolarity(review):
            return TextBlob(review).sentiment.polarity

        #memberi analysis score pada tiap sample
        def analys(score):
            if score < 0:
                return 'Negatif'
            elif score == 0:
                return 'Apatis'
            else:
                return 'Positif'

        #variable dibawah adalah bentuk akhir dataframe yang sudah bersih
        final_data = pd.DataFrame(df2[['date','username','Lemma']])

        anies = final_data.loc[df2['anies'] == 1]
        la = len(df2[df2['anies']==1])

        anies['Subjectivy'] = anies['Lemma'].apply(getSubjectivy)
        anies['Polarity'] = anies['Lemma'].apply(getPolarity)
        anies['TextBlob'] = anies['Polarity'].apply(analys)

        tb_counts_anies = anies.TextBlob.value_counts('')


        ganjar = final_data.loc[df2['ganjar'] == 1]
        lg = len(df2[df2['ganjar']==1])

        ganjar['Subjectivy'] = ganjar['Lemma'].apply(getSubjectivy)
        ganjar['Polarity'] = ganjar['Lemma'].apply(getPolarity)
        ganjar['TextBlob'] = ganjar['Polarity'].apply(analys)

        tb_counts_ganjar = ganjar.TextBlob.value_counts()

        lr=int(len(final_data))
        tgl_dari = final_data['date'].values[lr-1]
        yd = tgl_dari[:4]
        md = tgl_dari[5:7]
        td = tgl_dari[8:10]
        jd = tgl_dari[11:19]
        date = datetime.datetime.strptime(md,"%m")
        buland = date.strftime("%B")

        tgl_dari = final_data['date'].values[0]
        ys = tgl_dari[:4]
        ms = tgl_dari[5:7]
        ts = tgl_dari[8:10]
        js = tgl_dari[11:19]
        date = datetime.datetime.strptime(ms,"%m")
        bulans = date.strftime("%B")

        sl.write('****')

        sl.write('#### Hasil Analisis Sentimen Twitter dari tanggal ',td,buland,yd,'pukul',jd,'sampai dengan tanggal ',ts,bulans,ys,'pukul',js)
        sl.write('#### Data yang berhasil dikumpulkan sebanyak',lr)

        tgl_smp = final_data['date'].values[lr-1]
        # sl.write('dari ', tgl_dari,' sampai ',tgl_smp)



        sl.write("*****")

        c1, c2, c3 = sl.columns((4,1,4))
        with c1:
            sl.markdown('# Anies')
            piee = plt.figure(figsize=(3,5))
            piee.set_facecolor("darkgrey")
            pies = plt.pie(tb_counts_anies.values, labels=tb_counts_anies.index, explode=(0.1,0,0), autopct='%1.1f%%', shadow=False)
            sl.write(piee)

        with c3:
            sl.markdown('# Ganjar')
            piee = plt.figure(figsize=(3,5))
            piee.set_facecolor("darkgrey")
            pies = plt.pie(tb_counts_ganjar.values, labels=tb_counts_anies.index, explode=(0.1,0,0), autopct='%1.1f%%', shadow=False)
            sl.write(piee)

        sl.write("*****")

        cs1, cs2, cs3 = sl.columns((4,1,4,))

        with cs1:
            sl.write("##### Jumlah tweet tentang Anies : ",la)
            lpa = len(anies[anies['TextBlob']=='Positif'])
            lna = len(anies[anies['TextBlob']=='Negatif'])
            laa = len(anies[anies['TextBlob']=='Apatis'])
            
            sl.write('***')
            sl.write('Tweet Positif tentang Anies : ',lpa)
            my_pbar = sl.progress(0)
            for percent_complete in range(lpa):
                time.sleep(0.003)
                my_pbar.progress(percent_complete + 1)
                
            sl.write('Tweet Negatif tentang Anies : ',lna)
            my_nbar = sl.progress(0)
            for percent_complete in range(lna):
                time.sleep(0.003)
                my_nbar.progress(percent_complete + 1)
            
            sl.write('Tweet Apatis tentang Anies : ',laa)
            my_nbar = sl.progress(0)
            for percent_complete in range(laa):
                time.sleep(0.003)
                my_nbar.progress(percent_complete + 1)
            


        with cs3:
            sl.write("##### Jumlah tweet tentang Ganjar: ",lg)
            lpg = len(ganjar[ganjar['TextBlob']=='Positif'])
            lng = len(ganjar[ganjar['TextBlob']=='Negatif'])
            lag = len(ganjar[ganjar['TextBlob']=='Apatis'])
            
            sl.write('***')
            sl.write('Tweet Positif tentang Ganjar : ',lpg)
            my_pbar = sl.progress(0)
            for percent_complete in range(lpg):
                time.sleep(0.003)
                my_pbar.progress(percent_complete + 1)
                
            sl.write('Tweet Negatif tentang Ganjar : ',lng)
            my_nbar = sl.progress(0)
            for percent_complete in range(lng):
                time.sleep(0.003)
                my_nbar.progress(percent_complete + 1)
            
            sl.write('Tweet Apatis tentang Ganjar : ',lag)
            my_nbar = sl.progress(0)
            for percent_complete in range(lag):
                time.sleep(0.003)
                my_nbar.progress(percent_complete + 1)
            

        sl.write('*****')

        
        
        
    except Exception as e:
        print(e)
        df2 = pd.read_excel(uploaded_file)
