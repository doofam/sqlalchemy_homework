import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from pprint import pprint 

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.sql import label

from flask import Flask, jsonify, request

Base = declarative_base()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)

app = Flask(__name__)

class Measurement(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)

class Station(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)


@app.route("/")
def home():
    return (f"The Climate App<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation --> returns precipitation data in Hawaii by date<br/>"
        f"/api/v1.0/temperature --> returns temperature data in Hawaii by date <br/>"
        f"/api/v1.0/temps/<start> --> returns the average, min, and max temperature for all dates greater than and equal to the start date. <br/>"
        f"/api/v1.0/temps/<start>/<end> --> returns the average, min, and max temperature for dates between the start and end date inclusive. <br/>"
        f"<br/>"
        f"NOTE: Dates should be formatted YYYY-MM-DD")


@app.route("/api/v1.0/precipitation")
def get_prcp_data():
    prcp_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    return jsonify(prcp_data)


@app.route("/api/v1.0/temperature")
def get_temp_data():
    temp_data = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date).all()
    return jsonify(temp_data)  


temps = session.query(Measurement.date, Measurement.tobs).all()
df_temps = pd.DataFrame(temps)
df_temps.loc[:, "date"] = pd.to_datetime(df_temps["date"], yearfirst=True)


@app.route("/api/v1.0/<start>")
def calc_temps_1(start):
    df_start = df_temps.loc[df_temps["date"] >= datetime.strptime(start, "%Y-%m-%d")]
    return f"Average: {df_start['tobs'].mean()}, Min: {df_start['tobs'].min()}, Max: {df_start['tobs'].max()}"


@app.route("/api/v1.0/<start>/<end>")
def calc_temps_2(start, end):
    df_start_end = df_temps.loc[(df_temps["date"] >= datetime.strptime(start, "%Y-%m-%d"))\
         & (df_temps["date"] <= datetime.strptime(end, "%Y-%m-%d"))]
    return f"Average: {df_start_end['tobs'].mean()}, Min: {df_start_end['tobs'].min()}, Max: {df_start_end['tobs'].max()}"


if __name__ == "__main__":
    app.run(debug=True)