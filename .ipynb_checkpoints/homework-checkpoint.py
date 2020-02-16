import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from pprint import pprint 

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date

Base = declarative_base()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# inspector = inspect(engine)
	
# table_names = inspector.get_table_names()
# print(table_names)

# for table in table_names:
#     print(table + ":")
#     columns = inspector.get_columns(table)
#     pprint(columns)

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

session = Session(engine)

# ### Precipitation Analysis

# * Design a query to retrieve the last 12 months of precipitation data.
latest_date = session.query(func.max(Measurement.date)).first()
print(latest_date)

year_ago = datetime.date(2017, 8, 23) - datetime.timedelta(days=365)
lastest_year_data = session.query(Measurement.date).filter(Measurement.date > year_ago).order_by(Measurement.date).all()
print(lastest_year_data)

# * Select only the `date` and `prcp` values.
date_prcp_data = session.query(Measurement.date, Measurement.prcp).all()

# * Load the query results into a Pandas DataFrame and set the index to the date column.
df = pd.read_sql_query(date_prcp_data, con=engine)
print(df)

# * Sort the DataFrame values by `date`.
df.sort_values("date")

# * Plot the results using the DataFrame `plot` method.


# * Use Pandas to print the summary statistics for the precipitation data.

# ### Station Analysis

# * Design a query to calculate the total number of stations.

# * Design a query to find the most active stations.

#   * List the stations and observation counts in descending order.

#   * Which station has the highest number of observations?

#   * Hint: You may need to use functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in your queries.

# * Design a query to retrieve the last 12 months of temperature observation data (tobs).

#   * Filter by the station with the highest number of observations.

#   * Plot the results as a histogram with `bins=12`.

# - - -

# ## Step 2 - Climate App

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# * Use FLASK to create your routes.

# ### Routes

# * `/`

#   * Home page.

#   * List all routes that are available.

# * `/api/v1.0/precipitation`

#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

#   * Return the JSON representation of your dictionary.

# * `/api/v1.0/stations`

#   * Return a JSON list of stations from the dataset.

# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

# ## Hints

# * You will need to join the station and measurement tables for some of the analysis queries.

# * Use Flask `jsonify` to convert your API data into a valid JSON response object.

# - - -

# ### Optional: Other Recommended Analyses

# * The following are optional challenge queries. These are highly recommended to attempt, but not required for the homework.

# ### Temperature Analysis

# * The starter notebook contains a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d` and return the minimum, average, and maximum temperatures for that range of dates.

# * Use the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

# * Plot the min, avg, and max temperature from your previous query as a bar chart.

#   * Use the average temperature as the bar height.

#   * Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr).

#     ![temperature](Images/temperature.png)

# ### Daily Rainfall Average.

# * Calculate the rainfall per weather station using the previous year's matching dates.

# * Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

# * You are provided with a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic tobs that match that date string.

# * Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

# * Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

# * Use Pandas to plot an area plot (`stacked=False`) for the daily normals.

#   ![daily-normals](Images/daily-normals.png)
