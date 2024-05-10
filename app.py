from flask import Flask, render_template, request, jsonify
from flask_cors import CORS ,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import logging as lg
import pymongo

lg.basicConfig(level = lg.INFO, 
               filename = 'webscrap.log')

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")