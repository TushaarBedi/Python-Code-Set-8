# import all libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
import tushaar_scrape_mars
import os

app = Flask(__name__)


client = pymongo.MongoClient()
db = client.Mars_Database
collection = db.Mars_Data


@app.route("/scrape")
def scrape():
    mars_data_dict = tushaar_scrape_mars.scrape()
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        #collection.insert_one(mars_data_dict)

        collection.update(
            {},
            mars_data_dict,
            upsert=True
        )

    print("Flask Web Service Call for Data Scraping is complete!")
    return redirect("http://localhost:5000/", code=302)
    

# create route that renders index.html template
@app.route("/")
def index():
    Mars_Data_Output = collection.find_one()
    return render_template("index.html", Mars_Data_Output = Mars_Data_Output)


if __name__ == "__main__":
    app.run(debug=True)
