from scipy import stats
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#Creating our engine
engine = create_engine("sqlite:///../../../working/10-Advanced-Data-Storage-and-Retrieval/Homework/Instructions/Resources/hawaii.sqlite")

#Reflecting existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

#Home route
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

#Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    #Selecting date and prcp from Measurement
    date_prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    #Adding our dates and prcp values to a list
    prcp_list = []
    for date, prcp in date_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    #Returning the complete list
    return jsonify(prcp_list)

#Stations route
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    #Select station id from Station
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    #Return the list
    return jsonify(station_names)

#Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    most_active_id = "USC00519281"

    #Query for date and temp for most active id for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_id).filter(Measurement.date > '2016-8-23').filter(Measurement.date <= '2017-8-23').all()
    session.close()

    #Adding date and tobs values to list
    tobs_list = []
    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    #Returning list
    return jsonify(tobs_list)

#Route with start date
@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    #Creating function to get min, avg, and max for tobs values in Measurement
    funcs = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #Using these functions for dates greater than or equal to start date
    results = session.query(*funcs).filter(Measurement.date >= start).all()
    session.close()

    #Converting list of tuples into normal list
    temps = list(np.ravel(results))

    #Returning list
    return jsonify(temps)

#Route with start date and end date
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    session = Session(engine)

    #Creating function to get min, avg, and max for tobs values in Measurement
    funcs = [func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #Using these functions for dates between start and end date inclusive
    results = session.query(*funcs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    #Converting list of tuples into normal list
    temps = list(np.ravel(results))

    #Returning list
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)

