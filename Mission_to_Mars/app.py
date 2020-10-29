#import things
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# From the separate python file in this directory, we'll import the code that is used to scrape craigslist
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# render index.html with the Mars info in our database.
@app.route('/')
def index():

    mars_info = mongo.db.mars_info.find_one()
    return render_template('index.html', mars_info=mars_info)

#trigger webscraping 
@app.route('/scrape')
def scrape():

    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)

     # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")

  
     
  
    




if __name__ == "__main__":
    app.run(debug=True)