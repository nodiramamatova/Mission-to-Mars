# Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars
import pymongo

# create instance of Flask app
app = Flask(__name__)
mongo = PyMongo(app)

#Connect to MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

#  create route that renders index.html template
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape()
    mars.update(
                {},
                mars_data,
                upsert=True
                )
    return redirect("/", code=302)
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)



if __name__ == "__main__":
    app.run(debug=True)
