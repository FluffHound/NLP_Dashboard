from flask import Flask, redirect, url_for, request
from flask.templating import render_template
from numpy import random
import pandas as pd
import joblib
import requests


app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/aboutus')
def AboutUs():
    return render_template('About Us.html')

@app.route('/candidate')
def candidate():
    return render_template('Infopedia Kandidat.html')
@app.route('/anies')
def anies():
    calon = 'anies'
    ## LDA
    r2 = requests.post(
            "http://127.0.0.1:5000/api/LDA",
            json={"status": "minta datanya dong", "calon": calon},
        )
    save = open(f"static/iframeTM/lda_{calon}.html", "wb").write(r2.content)
    ## Wordcloud Sentiment
    waktu = ['All time','14 Hari','7 Hari','Hari ini']
    sent = ['pos','neg','neu']

    for i in waktu:
        for j in sent:
            r3 = requests.post(
            "http://127.0.0.1:5000/api/wordcloud", json={"status": "minta datanya dong", "calon": calon,'waktu':i,'sentiment':j},)
            save = open(f"static/assets/Wordcloud/{calon}/wordcloud_mention_{calon}_{i}_{j}.jpg", "wb").write(r3.content)
    
    ## Wordcloud Profile
    r4 = requests.post(
        "http://127.0.0.1:5000/api/wordcloudprofile",
        json={"status": "minta datanya dong", "calon": calon},
    )
    save = open(f"static/assets/Wordcloud/{calon}/wordcloud_profile_{calon}.jpg", "wb").write(r4.content)
    return render_template('Anies.html')
@app.route('/ahy')
def ahy():
    calon = 'ahy'
    ## LDA
    r2 = requests.post(
            "http://127.0.0.1:5000/api/LDA",
            json={"status": "minta datanya dong", "calon": calon},
        )
    save = open(f"static/iframeTM/lda_{calon}.html", "wb").write(r2.content)
    ## Wordcloud Sentiment
    waktu = ['All time','14 Hari','7 Hari','Hari ini']
    sent = ['pos','neg','neu']

    for i in waktu:
        for j in sent:
            r3 = requests.post(
            "http://127.0.0.1:5000/api/wordcloud", json={"status": "minta datanya dong", "calon": calon,'waktu':i,'sentiment':j},)
            save = open(f"static/assets/Wordcloud/{calon}/wordcloud_mention_{calon}_{i}_{j}.jpg", "wb").write(r3.content)
    
    ## Wordcloud Profile
    r4 = requests.post(
        "http://127.0.0.1:5000/api/wordcloudprofile",
        json={"status": "minta datanya dong", "calon": calon},
    )
    save = open(f"static/assets/Wordcloud/{calon}/wordcloud_profile_{calon}.jpg", "wb").write(r4.content)
    return render_template('AHY.html')
@app.route('/ganjar')
def ganjar():
    calon = 'ganjar'
    ## LDA
    r2 = requests.post(
            "http://127.0.0.1:5000/api/LDA",
            json={"status": "minta datanya dong", "calon": calon},
        )
    save = open(f"static/iframeTM/lda_{calon}.html", "wb").write(r2.content)
    ## Wordcloud Sentiment
    waktu = ['All time','14 Hari','7 Hari','Hari ini']
    sent = ['pos','neg','neu']

    for i in waktu:
        for j in sent:
            r3 = requests.post(
            "http://127.0.0.1:5000/api/wordcloud", json={"status": "minta datanya dong", "calon": calon,'waktu':i,'sentiment':j},)
            save = open(f"static/assets/Wordcloud/{calon}/wordcloud_mention_{calon}_{i}_{j}.jpg", "wb").write(r3.content)
    
    ## Wordcloud Profile
    r4 = requests.post(
        "http://127.0.0.1:5000/api/wordcloudprofile",
        json={"status": "minta datanya dong", "calon": calon},
    )
    save = open(f"static/assets/Wordcloud/{calon}/wordcloud_profile_{calon}.jpg", "wb").write(r4.content)
    return render_template('Ganjar.html')
@app.route('/prabowo')
def prabowo():
    calon = 'prabowo'
    ## LDA
    r2 = requests.post(
            "http://127.0.0.1:5000/api/LDA",
            json={"status": "minta datanya dong", "calon": calon},
        )
    save = open(f"static/iframeTM/lda_{calon}.html", "wb").write(r2.content)
    ## Wordcloud Sentiment
    waktu = ['All time','14 Hari','7 Hari','Hari ini']
    sent = ['pos','neg','neu']

    for i in waktu:
        for j in sent:
            r3 = requests.post(
            "http://127.0.0.1:5000/api/wordcloud", json={"status": "minta datanya dong", "calon": calon,'waktu':i,'sentiment':j},)
            save = open(f"static/assets/Wordcloud/{calon}/wordcloud_mention_{calon}_{i}_{j}.jpg", "wb").write(r3.content)
    
    ## Wordcloud Profile
    r4 = requests.post(
        "http://127.0.0.1:5000/api/wordcloudprofile",
        json={"status": "minta datanya dong", "calon": calon},
    )
    save = open(f"static/assets/Wordcloud/{calon}/wordcloud_profile_{calon}.jpg", "wb").write(r4.content)
    return render_template('Prabowo.html')
@app.route('/ridwan')
def rk():
    calon = 'rk'
    ## LDA
    r2 = requests.post(
            "http://127.0.0.1:5000/api/LDA",
            json={"status": "minta datanya dong", "calon": calon},
        )
    save = open(f"static/iframeTM/lda_{calon}.html", "wb").write(r2.content)
    ## Wordcloud Sentiment
    waktu = ['All time','14 Hari','7 Hari','Hari ini']
    sent = ['pos','neg','neu']

    for i in waktu:
        for j in sent:
            r3 = requests.post(
            "http://127.0.0.1:5000/api/wordcloud", json={"status": "minta datanya dong", "calon": calon,'waktu':i,'sentiment':j},)
            save = open(f"static/assets/Wordcloud/{calon}/wordcloud_mention_{calon}_{i}_{j}.jpg", "wb").write(r3.content)
    
    ## Wordcloud Profile
    r4 = requests.post(
        "http://127.0.0.1:5000/api/wordcloudprofile",
        json={"status": "minta datanya dong", "calon": calon},
    )
    save = open(f"static/assets/Wordcloud/{calon}/wordcloud_profile_{calon}.jpg", "wb").write(r4.content)
    return render_template('Ridwan Kamil.html')


if __name__ == '__main__':
    app.run(debug = True,port=80)
