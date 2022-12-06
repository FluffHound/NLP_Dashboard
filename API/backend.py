import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("project-nlp-9b41d-firebase-adminsdk-w4jxt-038c435e97.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  # this connects to our Firestore database


def scraper(katakunci):
    ## SCRAPER


    ## Store to DB
    sentiment = db.collection('Sentiment')
    doc = sentiment.document(katakunci)
    res = doc.get().to_dict()
    data = {'id':res['id']+list(df['id']),
                  'datetime':res['datetime']+list(df['datetime']),
                  'username':res['username']+list(df['username']),
                  'content':res['content']+list(df['content']),
                  'clean_text':res['clean_text']+list(df['clean_text']),
                  'clean_text_stem':res['clean_text_stem']+list(df['clean_text_stem'])}
    sentiment = db.collection(u'Sentiment')
    sentiment.document(u'AHY').set(data)
    print("Data berhasil disimpan dalam database!")



def sentiment(katakunci):
    sentiment = db.collection('Sentiment')
    doc = sentiment.document(katakunci)
    res = doc.get().to_dict()
    df = pd.DataFrame(res)
    df['datetime'] = df.datetime.apply(lambda x: x.date())

    day7 = df[(df['datetime'] >= (datetime.now()-timedelta(days=7)).date()) & (df['datetime'] < (datetime.now()).date())]
    day3 = df[(df['datetime'] >= (datetime.now()-timedelta(days=3)).date()) & (df['datetime'] < (datetime.now()).date())]
    now = df[(df['datetime'] == (datetime.now()).date())]

    # PREDICT MODEL
    ## All time

    pred_all = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}
    ## 7 days

    pred_7 = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}
    ## 3 days

    pred_3 = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}

    ## Today
    pred_today = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}
    
    pred = {'All Time':pred_all,
            '7 Days':pred_7,
            '3 Days':pred_3,
            'Today':pred_today}
    db.collection(u'Prediksi Sentimen').document(katakunci).set(pred)

    print("Hasil Sentiment Selesai!")


def LDA(katakunci):
    sentiment = db.collection('LDA')
    doc = sentiment.document(katakunci)
    res = doc.get().to_dict()
    df = pd.DataFrame(res)
    df['datetime'] = df.datetime.apply(lambda x: x.date())

    day7 = df[(df['datetime'] >= (datetime.now()-timedelta(days=7)).date()) & (df['datetime'] < (datetime.now()).date())]
    day3 = df[(df['datetime'] >= (datetime.now()-timedelta(days=3)).date()) & (df['datetime'] < (datetime.now()).date())]
    now = df[(df['datetime'] == (datetime.now()).date())]


def wordcloud(katakunci):
    # Wordcloud Sentiment
    sentiment = db.collection('Sentiment')
    doc = sentiment.document(katakunci)
    res = doc.get().to_dict()
    df = pd.DataFrame(res)
    df['datetime'] = df.datetime.apply(lambda x: x.date())

    day7 = df[(df['datetime'] >= (datetime.now()-timedelta(days=7)).date()) & (df['datetime'] < (datetime.now()).date())]
    day3 = df[(df['datetime'] >= (datetime.now()-timedelta(days=3)).date()) & (df['datetime'] < (datetime.now()).date())]
    now = df[(df['datetime'] == (datetime.now()).date())]

    # Wordcloud LDA
    sentiment = db.collection('LDA')
    doc = sentiment.document(katakunci)
    res = doc.get().to_dict()
    df = pd.DataFrame(res)
    df['datetime'] = df.datetime.apply(lambda x: x.date())

    day7 = df[(df['datetime'] >= (datetime.now()-timedelta(days=7)).date()) & (df['datetime'] < (datetime.now()).date())]
    day3 = df[(df['datetime'] >= (datetime.now()-timedelta(days=3)).date()) & (df['datetime'] < (datetime.now()).date())]
    now = df[(df['datetime'] == (datetime.now()).date())]




hashtags = ['ganjarpranowofor2024', 'prabowo', 'AniesPresiden2024', 'AHY', 'RidwanKamil']
usernames = ['ganjarpranowo', 'prabowo', 'aniesbaswedan', 'AgusYudhoyono', 'ridwankamil']
keywords = ['@ganjarpranowo', '@prabowo', '@aniesbaswedan', '@AgusYudhoyono', '@ridwankamil']



    
    





