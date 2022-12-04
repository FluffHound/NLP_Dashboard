from flask import Flask, redirect, url_for, request
from flask.templating import render_template
from numpy import random
import pandas as pd
import joblib

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
    return render_template('Anies.html')
@app.route('/AHY')
def ahy():
    return render_template('AHY.html')
@app.route('/ganjar')
def ganjar():
    return render_template('Ganjar.html')
@app.route('/prabowo')
def prabowo():
    return render_template('Prabowo.html')
@app.route('/ridwank')
def rk():
    return render_template('Ridwan Kamil.html')


if __name__ == '__main__':
    app.run(debug = True)
