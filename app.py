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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
inspector = inspect(engine)
inspector.get_table_names()
# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station=Base.classes.station

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
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
 
  
    
    #Query all passengers
    results = session.query(Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))

    #Return the JSON representation of your dictionary."""

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
 
  
    
    #Query all passengers
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-18").all()


    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    #Return the JSON representation of your dictionary."""

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start():
    def calc_temps(start_date, end_date):
     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

if __name__ == '__main__':
    app.run(debug=True)