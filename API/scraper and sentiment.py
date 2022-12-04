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
    doc = sentiment.document('AHY')
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

    day7 = df[(df['datetime'] > (datetime.now()-timedelta(days=7)).date()) & (df['datetime'] < (datetime.now()).date())]
    day3 = df[(df['datetime'] > (datetime.now()-timedelta(days=3)).date()) & (df['datetime'] < (datetime.now()).date())]
    now = df[(df['datetime'] == (datetime.now()).date())]

    # PREDICT MODEL
    ## All time

    pred = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}
    db.collection(u'Prediksi Sentimen').document(u'All Time').set(pred)
    ## 7 days

    pred = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}
    db.collection(u'Prediksi Sentimen').document(u'7 Days').set(pred)
    ## 3 days

    pred = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}
    db.collection(u'Prediksi Sentimen').document(u'3 Days').set(pred)

    ## Today
    pred = {"last_update":datetime.now(),
        "Positif":1000,
        "Netral":20,
        "Negatif":100}

    db.collection(u'Prediksi Sentimen').document(u'Today').set(pred)

    print("Hasil Sentiment Selesai!")





