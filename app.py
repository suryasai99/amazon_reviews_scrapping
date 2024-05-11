from flask import Flask, render_template, request, jsonify
from flask_cors import CORS ,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import logging as lg
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

lg.basicConfig(level = lg.INFO, 
               filename = 'webscrap.log')

app = Flask(__name__)

@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review", methods = ['POST' , 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(" ","")
            amazon_url = f"https://www.amazon.in/s?k={search_string}" 
            am_html = bs(ureq(amazon_url).read(), 'html.parser')
            find_loc_link = am_html.find_all("a",{"class":"a-link-normal s-no-outline"})
            product_link = f"https://www.amazon.in/{find_loc_link[0]['href']}"
            print(len(find_loc_link))
            product_info = bs(ureq(product_link).read(), "html.parser")
            full_info = product_info.find_all('div',{"class":'a-section review aok-relative'})
            
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
                
                everything = {
                    "product":search_string,
                    "name": name,
                    "rating": rating,
                    "review_title": review_title,
                    "review_date": review_date,
                    "comment": comment
                    }
                reviews.append(everything)
            lg.info(f"my final result{reviews}")

            # connecting to a pymongo database
            uri = "mongodb+srv://suryakadali1994:btbSZNLdUxGUmWMT@mydatabase.bzm4fk7.mongodb.net/?retryWrites=true&w=majority&appName=mydatabase"
            # Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))
            db = client['amazon_reviews_scrapping']
            collections = db['r_scrapping']
            collections.insert_many(reviews)

            return render_template('result.html', reviews=reviews[0:(len(reviews))])
        
        except Exception as e:
            lg.info(e)
            return 'check your code'
    else:
        return render_template('index.html')

if __name__ =="__main__":
    
    app.run(host = "0.0.0.0",port=5070)