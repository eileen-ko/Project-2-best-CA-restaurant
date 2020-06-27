city = ["Atherton", "Belmont", "Brisbane", "Burlingame", "Colma", "Daly City", "East Palo Alto", "Foster City",  "Half Moon Bay", "Menlo Park", "Millbrae", "Pacifica", "Portola Valley", "Redwood City", "San Bruno", "San Carlos", "San Francisco", "San Mateo", "South San Francisco", "Woodside", "Campbell", "Cupertino", "Gilroy", "Los Altos", "Milpitas", "Monte Sereno", "Morgan Hill", "Mountain View", "Palo Alto", "San Jose", "Santa Clara", "Saratoga", "Sunnyvale"]

import os

import pandas as pd
import numpy as np


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import MetaData

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sf_restaurant_db.sqlite"
db = SQLAlchemy(app)
# engine = create_engine("sqlite:///sf_restaurant_db.sqlite", connect_args = {"check_same_thread": False})
# reflect an existing database into a new model
db.init_app(app)
#meta = MetaData()
db.metadata.reflect(bind=db.engine)
print(db.metadata.tables.keys())

Base = automap_base()
# reflect the tables
#Base.prepare(db.engine, reflect=True)



# Save references to each table
#restaurant_info = Base.classes.restaurant_info
restaurant_info = db.metadata.tables['restaurant_info']
#session = Session(engine)



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/test")
def testRoute():
    return jsonify(db.session.query(restaurant_info).all())


@app.route("/<city>/<category>")
def city_restaurant(city,category):
    """Return the MetaData for a given sample."""
    sel = [
        restaurant_info.c.Business_Name, 
        restaurant_info.c.Review_Count,
        restaurant_info.c.Average_Rating,
        restaurant_info.c.Category,
        restaurant_info.c.Latitude,
        restaurant_info.c.Longtitude,
        restaurant_info.c.Address,
        restaurant_info.c.City,
        restaurant_info.c.Zip_Code,
        restaurant_info.c.Phone_Number,
    ]

    #return jsonify(db.session.query(restaurant_info).filter(restaurant_info.c.City == city).all())


    if category == "All":
        results = db.session.query(*sel).filter(restaurant_info.c.City == city).all()
    else:
        results = db.session.query(*sel).filter(restaurant_info.c.City == city).filter(restaurant_info.c.Category == category).all()



    # Create a list for each row of metadata information
    city_restaurant = []
    for result in results:
        restaurant = {}
        restaurant["Restaurant Name"] = result[0]
        restaurant["Review"] = result[1]
        restaurant["Average Rating"] = result[2]
        restaurant["Latitude"] = result[3]
        restaurant["Longtitude"] = result[4]
        restaurant["Address"] = result[5]
        restaurant["City"] = result[6]
        restaurant["Zip_Code"] = result[7]
        restaurant["Phone_Number"] = result[8]
        city_restaurant.append(restaurant)

    print(city_restaurant)
    return jsonify(city_restaurant)


if __name__ == "__main__":
    app.run()
