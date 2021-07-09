  
import numpy as np
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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
  session = Session(engine)
  results = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= "2016-08-24").\
      all()

  session.close()
  
  # Convert the list to Dictionary
  all_prcp = []
  for date,prcp  in results:
      prcp_dict = {}
      prcp_dict["date"] = date
      prcp_dict["prcp"] = prcp
              
      all_prcp.append(prcp_dict)

  return jsonify(Percipitation=all_prcp)

@app.route("/api/v1.0/stations")
def stations():
  session = Session(engine)
  results = session.query(Station.station).all()

  session.close()
# Return a JSON list of stations from the dataset.
  return jsonify(all_stations=results)


@app.route("/api/v1.0/tobs")
def tobs():
  session = Session(engine)
  results = session.query(Measurement.tobs).\
                          filter(Measurement.date >= "2016-08-24").\
                          filter(Measurement.date <= "2017-08-23").\
                          filter(Measurement.station == 'USC00519281').all()

  session.close()
# Return a JSON list of stations from the dataset.
  return jsonify(tobs=results)

@app.route("/api/v1.0/<start>") 
def Start_date_fn(start):
  session = Session(engine)
  results = session.query(func.min(Measurement.tobs),
                func.max(Measurement.tobs),
                func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

  session.close()

  return jsonify(start_date_tobs=results)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
  session = Session(engine)
  results = session.query(func.min(Measurement.tobs),
                func.max(Measurement.tobs),
                func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

  session.close()

  return jsonify(start_end_date_tobs=results)

if __name__ == "__main__":
  app.run(debug=True)