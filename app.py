import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)


# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station=Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Precipitation query
    results = session.query(Measurement.prcp).all()

    # Convert to list
    all_precipitation = list(np.ravel(results))

    #Return the JSON representation

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    #Return the JSON representation

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    #Query tobs
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-18").all()

    # Convert to list
    all_tobs = list(np.ravel(results))

    #Return the JSON representation

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    result =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date == start).all()
    
    # Convert to list
    result = list(np.ravel(result))

    #Return the JSON representation
    return jsonify(result)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Convert to list
    result = list(np.ravel(result))

    #Return the JSON representation
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)