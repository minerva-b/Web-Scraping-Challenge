# Import dependencies:
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask:
app = Flask(__name__)

# Use PyMongo to establish Mongo connection:
mongo = PyMongo(app, uri="mongodb://localhost:27017/misson_mars_app")


# Route to render index.html template using data from Mongo:
@app.route("/")
def home():

    # Find the existing mars collection from the mongo database, if not it will create one:
    mission_data = mongo.db.collection.find_one()

    # Return template and data. Set the variable mars equal to the data from the database
    return render_template("index.html", mars=mission_data)

# Route that will trigger the scrape function:
@app.route("/scrape")
def scrape():

    # Run the scrape function:
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True:
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page:
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)