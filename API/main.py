from flask import Flask,request, jsonify, abort, send_file
from flask_cors import CORS
import json

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
from backend import *

cred = credentials.Certificate("project-nlp-9b41d-firebase-adminsdk-w4jxt-038c435e97.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  # this connects to our Firestore database


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return '''<h1>Bicara Pilpres API v1</h1>'''
	

@app.route('/api/sentiment', methods=['POST'])
def req_data():
    if not request.json or not 'status' in request.json:
        abort(400)
    else:
        data = request.get_json()
        if data['status'] != 'minta datanya dong':
            abort(400)
        else:
            while True:
                calon = data['calon']
                dbs = db.collection('Sentiment')
                doc = dbs.document(calon)
                res = doc.get().to_dict()
                datetime_object = datetime.strptime(res['tanggal'], '%d/%m/%Y').date()
                if datetime_object < date.today():
                    sentiment(calon)
                    continue
                else:
                    break
            return jsonify(sentiment),201

@app.route('/api/LDA', methods=['POST'])
def req_forecast():
    if not request.json or not 'status' in request.json:
        abort(400)
    else:
        data = request.get_json()
        if data['status'] != 'minta datanya dong':
            abort(400)
        else:
            credentials = service_account.Credentials.from_service_account_file("project-nlp-9b41d-firebase-adminsdk-w4jxt-038c435e97.json")
            while True:
                calon = data['calon']
                storage.Client(credentials=credentials).bucket(firebase_admin.storage.bucket().name).blob(f'LDA HTML/lda_{calon}.html').download_to_filename(f'LDA HTML/lda_{calon}.html')
                forecast = dict(f.val())
                datetime_object = datetime.strptime(forecast['date'], '%d/%m/%Y').date()
                if datetime_object < date.today():
                    forecast_SVR(coin)
                    continue
                else:
                    break
            return jsonify(forecast),201

@app.route('/api/wordcloud', methods=['POST'])
def get_image():
    if not request.json or not 'status' in request.json:
        abort(400)
    data = request.get_json()
    if data['status'] != 'minta datanya dong':
            abort(400)
    else:
        config = {'apiKey': "AIzaSyBF9zZqQBt2h0RJZN3Xubugse5Ba3qJLdw",
            'authDomain': "elevate-66775.firebaseapp.com",
            'projectId': "elevate-66775",
            'databaseURL': "https://elevate-66775-default-rtdb.asia-southeast1.firebasedatabase.app/",
            'storageBucket': "elevate-66775.appspot.com",
            'messagingSenderId': "1008765930388",
            'appId': "1:1008765930388:web:5ad1f3c8464d8f8d859d81",
            'measurementId': "G-0Q4Y5MFCVD"}
        firebase = pyrebase.initialize_app(config)
        # Get a reference to the auth service
        auth = firebase.auth()
        email = 'alfianp613@gmail.com'
        password = 'DummyDummy631'
        # Log the user in
        user = auth.sign_in_with_email_and_password(email, password)
        while True:
            coin = data['koin']
            database = firebase.database()
            f = database.child("Sentiment").child(coin).get(user['idToken'])
            sentiment = dict(f.val())
            datetime_object = datetime.strptime(sentiment['tanggal'], '%d/%m/%Y').date()
            if datetime_object < date.today():
                sentimen(coin)
                continue
            else:
                break
        koin = data['koin']
        storage = firebase.storage()
        storage.child(f'wordcloud/wordcloud {koin}.png').download(f"wordcloud/wordcloud {koin}.png")
        return send_file(f'wordcloud/wordcloud {koin}.png', mimetype=f'image/png')

if __name__ == '__main__':
    app.run(debug=True)