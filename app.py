# Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# create instance of Flask app
app = Flask(__name__)
mongo = PyMongo(app)

#  create route that renders index.html template
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

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


if __name__ == "__main__":
    app.run(debug=True)
