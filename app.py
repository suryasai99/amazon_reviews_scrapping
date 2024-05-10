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

@app.route("/review", methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(" ","")
            amazon_url = f"https://www.amazon.in/s?k={search_string}" 
            am_html = bs(ureq(amazon_url).read(),
                         'html.parser')
            find_loc_link = am_html.find_all('div',
                                             {"class":"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"})
            product_link = f"https://www.amazon.in/{find_loc_link[0].a['href']}"
            
            product_info = bs(requests.get(product_link).text,
                              "html.parser")
            full_info = product_info.find_all('div',
                                              {"class":'a-section review aok-relative'})
            
            reviews = []
            for i in full_info:
                # to get name of the reviewer
                try:
                    name = i.div.div.div.find_all('div',{"class":'a-profile-content'})[0].text
                
                except:
                    lg.info("name")

                # To get the rating
                try:
                    rating = i.find_all('span')[1].text

                except:
                    lg.info("rating")

                # To get the review title
                try:
                    review_title = i.find_all('span')[3].text
                except:
                    lg.info('review_title')

                # TO get the review date
                try:
                    review_date = i.find_all('span')[4].text
                except:
                    lg.info('review_date')

                # To get comments
                try:
                    comment = i.find_all('span')[8].text
                except:
                    lg.info('comment')
                
                





if __name__ =="__main__":
    app.run(host = "0.0.0.0",port=5070)