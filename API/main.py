from flask import Flask,request, jsonify, abort, send_file
from flask_cors import CORS
import json
import pyrebase
from SVR import *
from sentiment import *
from datetime import datetime, timedelta
import investpy


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return '''<h1>Elevate API v1</h1>'''
	

@app.route('/api/datasentiment', methods=['POST'])
def req_data():
    if not request.json or not 'status' in request.json:
        abort(400)
    else:
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
            return jsonify(sentiment),201

@app.route('/api/forecast', methods=['POST'])
def req_forecast():
    if not request.json or not 'status' in request.json:
        abort(400)
    else:
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
                f = database.child("Forecast").child(coin).get(user['idToken'])
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

@app.route('/api/historicaldata', methods=['POST'])
def historical():
    if not request.json or not 'koin' in request.json:
        abort(400)
    else:
        data = request.get_json()
        koin = data['koin']
        sekarang = datetime.now().strftime("%d/%m/%Y")
        kemarin = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        data = investpy.get_crypto_historical_data(crypto=koin,
                                            from_date=kemarin,
                                            to_date=sekarang)
        
        x = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        y = data['Close'][-1]
        results = {'date': x, 'value': y}
        return jsonify(results), 201

if __name__ == '__main__':
    app.run(debug=True)