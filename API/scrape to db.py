# ===========================
# ===== Import Packages =====
# ===========================
import pandas as pd
import numpy as np
from tqdm import tqdm

import snscrape.modules.twitter as sntwitter

import re, string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pyrebase

# ___Remove Rubbish___
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub("@[A-Za-z0-9_]+", "", text)  # Menghapus @<name> [mention twitter]
    text = re.sub("#\w+", "", text) # Menghapus hashtag #
    text = re.sub("\[.*?\]", "", text)  # Menghapus [string]
    text = re.sub("https?://\S+|www\.\S+", "", text)    # Menghapus link
    text = re.sub("<.*?>+", "", text)   # Menghapus <string>
    text = re.sub("[%s]" % re.escape(string.punctuation), "", text) # Menghapus tanda baca
    text = re.sub("\w*\d\w*", "", text) # Menghapus kata + angka ex: t0g3l
    text = re.sub("\d+", "", text)  # Menghapus kata diawali huruf ex: 45merdeka
    text = re.sub("amp", " ", text) # Menghapus &amp; pada kata
    text = re.sub("\s+", " ", text).strip() # Menghapus whitespace di antara kata
    text = text.replace("\n", " ")  # Menghapus tag newline
    text = " ".join(text.split())
    return text

# ___Stemming___
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ___Stopword___
factory_stop = StopWordRemoverFactory()
stopword = factory_stop.create_stop_word_remover()

# ___Tokenizing___
def word_tokenize_wrapper(text):
  return word_tokenize(text)

def sentimen(katakunci):
    # Scrape Hashtag Tweet
    tweets_list = []

    for i, tweet in enumerate(tqdm(sntwitter.TwitterHashtagScraper(katakunci).get_items())):
        if i > 50:
            break
        tweets_list.append([tweet.id, tweet.date, tweet.user.username, tweet.content])

    tweets_df = pd.DataFrame(tweets_list, columns=['ID', 'Datetime', 'Username', 'Content'])

    # ___Cleaning, Stemming, Remove Stopwords, Remove Blank Text, Tokenize___
    tweets_df['clean_text'] = tweets_df['Content'].apply(lambda x: clean_text(x))
    tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: stemmer.stem(x))
    tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: stopword.remove(x))
    tweets_df.replace("", float("NaN"), inplace=True)
    tweets_df = tweets_df.dropna()
    tweets_df['text_token'] = tweets_df['clean_text'].apply(word_tokenize_wrapper)
    tweets_df['Datetime'] = tweets_df['Datetime'].apply(lambda x: x.strftime('%Y/%m/%d'))

    # save in firebase
    config = {'apiKey': "AIzaSyBnNNm38XJJb0D5QVIYNkOKaOb5Ie58vQs",
              'authDomain': "project-nlp-9b41d.firebaseapp.com",
              'databaseURL': "https://project-nlp-9b41d-default-rtdb.asia-southeast1.firebasedatabase.app",
              'projectId': "project-nlp-9b41d",
              'storageBucket': "project-nlp-9b41d.appspot.com",
              'messagingSenderId': "1043773135025",
              'appId': "1:1043773135025:web:a89bc3ca6e49f56f7b6a90",
              'measurementId': "G-B4WFSGLXGD"
            }
    firebase = pyrebase.initialize_app(config)
    # Get a reference to the auth service
    auth = firebase.auth()

    email = 'alfianp613@gmail.com'
    password = 'admin123'
    # # Log the user in
    user = auth.sign_in_with_email_and_password(email, password)
    database = firebase.database()
    r = database.child("Dataset").child("Sentiment").child(katakunci).get(user['idToken'])
    res = dict(r.val())
    tweet_final = {'id':res['id']+list(tweets_df['ID']),
                      'timestamp':res['timestamp']+list(tweets_df['Datetime']),
                      'username':res['username']+list(tweets_df['Username']),
                      'content':res['content']+list(tweets_df['Content']),
                      'cleantext':res['cleantext']+list(tweets_df['clean_text'])}
    a = database.child("Dataset").child("Sentiment").child(katakunci).set(tweet_final,user['idToken'])
    
    # storage = firebase.storage()
    # path_on_cloud = f"wordcloud/wordcloud {katakunci}.png"
    # path_local = f'wordcloud/wordcloud {katakunci}.png'
    
    # storage.child(path_on_cloud).put(path_local, user['idToken'])
    
    return print(f'sentiment {katakunci} Selesai')
