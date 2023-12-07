from application import app # Import the Flask app instance
from flask import render_template, request, json, jsonify
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import requests
import numpy
import pandas as pd
from flask import Flask, jsonify


uber_df = pd.read_csv("./uberdata/My Uber Drives - 2016.csv")
# print(uber_df)


app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
