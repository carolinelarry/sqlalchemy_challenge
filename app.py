import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../../../working/10-Advanced-Data-Storage-and-Retrieval/Homework/Instructions/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    #Select date and prcp from Measurement
    date_prcp = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    prcp_list = []
    for date, prcp in date_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers

    #Select name from Passenger
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #results = session.query(Station.station).all()
    #stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    most_active_id = "USC00519281"

    #Changing date column to a datetime column
    #measurement_df['date'] = pd.to_datetime(measurement_df['date'])

    #Finding our most recent date
    #start_date = measurement_df['date'].max()
    #end_date = start_date - dt.timedelta(days=365)

    #start_date = start_date.strftime("%Y-%m-%d")
    #end_date = end_date.strftime("%Y-%m-%d")


    #If the dates need to not be hardcoded: look at 10, Day 3, 02 activity

    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date < '2016-8-23').filter(Measurement.date >= '2017-8-23').filter_by(station == most_active_id).all()
    session.close()

    last_year_temps = list(np.ravel(results))

    return jsonify(last_year_temps)

#Copied code here
#========================================================
#@app.route("/api/v1.0/justice-league/<real_name>")
#def justice_league_character(real_name):
#    """Fetch the Justice League character whose real_name matches
#       the path variable supplied by the user, or a 404 if not."""

#    canonicalized = real_name.replace(" ", "").lower()
 #   for character in justice_league_members:
 #       search_term = character["real_name"].replace(" ", "").lower()

  #      if search_term == canonicalized:
  #          return jsonify(character)

   # return jsonify({"error": f"Character with real_name {real_name} not found."}), 404
#========================================================


#OTHER CODDDEEEEE: NOT MINE
#def toDate(dateString): 
    #return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
 
#@app.route()
#def event():
 #   ektempo = request.args.get('start', default = datetime.date.today(), type = toDate)
#END OF CODE: NOT MINE

#STart of my code
@app.route("/api/v1.0/<start>")
def start_date(start):
    #how to change the format on a Measurement.station to datetime thing

    start = start.strftime("%Y-%m-%d")

    results = session.query(Measurement.date, Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    start_date_temps = list(np.ravel(results))
    return jsonify(start_date_temps)

if __name__ == "__main__":
    app.run(debug=True)