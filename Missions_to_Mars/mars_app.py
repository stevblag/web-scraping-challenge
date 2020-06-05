from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask instance
app = Flask(__name__)

# PyMongo <> MongoDB connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Render index.html template w/ data from MongoDB
@app.route("/")
def home(): 

    # Find data
    mars_facts = mongo.db.collection.find_one()

    # Return template & data
    return render_template("index.html", mars=mars_facts)

# Trigger scrape
@app.route("/scrape")
def scrape():

    # Run scrape
    mars_data = scrape_mars.scrape()

    # Update MongoDB (upsert=True)
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
