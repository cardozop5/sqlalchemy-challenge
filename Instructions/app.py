import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
#from app import routes
import  matplotlib.pyplot as plt 

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

# save our ref's
Measurements = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)

app = Flask(__name__)
most_recent_date = session.query(func.max(Measurements.date)).first()[0]

most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")

most_recent_year = int(dt.datetime.strftime(most_recent_date, "%Y"))

most_recent_month = int(dt.datetime.strftime(most_recent_date, "%m"))

most_recent_day = int(dt.datetime.strftime(most_recent_date, "%d"))
most_recent_date
most_recent_year
most_recent_month
most_recent_day

prev_year = dt.date(most_recent_year, most_recent_month,
                    most_recent_day)-dt.timedelta(days=365)
most_recent_year = int(dt.datetime.strftime(most_recent_date, "%Y"))


@app.route("/")
def home():

    return(f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"<br/>"
        f" The List of stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f" List of temperature data<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"Min, Max and Avg temprature for given start or start-end range<br/>"
        f"/api/v1.0/start/end"
        f" Min, Avg, and maximum temperatures for a specified range of dates<br/>"
   )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session
    precp_data = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= prev_year).\
    order_by(Measurements.date).all()
    return jsonify(precp_data, label='prcp')

@app.route("/api/v1.0/stations")
def stations():
    result=session.query(Stations.name, Stations.station,
                         Stations.elevation).all()
    return jsonify([station[0] for station in result])

@app.route("/api/v1.0/tobs")
def tobs():
    result=session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= prev_year).\
        order_by(Measurements.date).all()
    return jsonify(result, label='tobs')

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    result=session.query(Measurements.date, func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).group_by(Measurements.date).all()
    result_list=list(result)
    return jsonify(result_list)

@app.route("/api/v1.0/<start>/<end>")
def temps(start=None, end=None):
    result=session.query(func.avg(Measurements.tobs), func.max(Measurements.tobs), func.min(Measurements.tobs), Measurements.date).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).group_by(Measurements.date).all
    result_list=list(result)
    return jsonify(result_list)

if __name__ == "__main__":
    app.run(debug=True)
