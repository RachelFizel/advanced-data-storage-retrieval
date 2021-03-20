
#################################################
# import Flask and needed things
#################################################
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Define what to do when a user hits the / or index route
@app.route("/")
def welcome():
    """List all available api routes."""
    print("Server received request")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end><br/>"
    )

# Define what to do when
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)


# Define what to do when
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    
    station_dic = {
        "station": all_names
    }
    
    return jsonify(station_dic)


# Define what to do when
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_recent = session.query(func.max(Measurement.date)).first()
    date_most_recent = dt.datetime.strptime(most_recent[0], '%Y-%m-%d')
    date_year_ago = date_most_recent-dt.timedelta(365)
        
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date>=date_year_ago).all()
    session.close()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)


# Define what to do when
@app.route("/api/v1.0/temp/<start_date>")
def temp_start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

        
    """Return a list of all stations"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs))\
                            .filter(Measurement.date >= start_date).all()
    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))

    temp_dict = {}
    temp_dict['min'] = all_temps[0]
    temp_dict['max'] = all_temps[1]
    temp_dict['avg'] = all_temps[2]
    
    return jsonify(temp_dict)

# Define what to do when
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def temp_start_end(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
        
    """Return a list of all stations"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs))\
                            .filter(Measurement.date >= start_date)\
                            .filter(Measurement.date <= end_date).all()
    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))

    temp_dict = {}
    temp_dict['min'] = all_temps[0]
    temp_dict['max'] = all_temps[1]
    temp_dict['avg'] = all_temps[2]
    
    return jsonify(temp_dict)

#################################################
# Flask Closing Code
#################################################
if __name__ == "__main__":
    app.run(debug=True)