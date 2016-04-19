from flask import Flask, render_template
from flask import g
from flask import jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

DATABASE = 'dbike_masterDB_test.db'

def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.route('/')
def hello():
    cur = get_db().cursor()
    #display web page
    return render_template('dublinbikes.html')


@app.route("/_station/<int:station_id>", methods= ['GET'])
def get_station_info(station_id):
    conn = get_db()

    #execute SQL query and create pandas dataframe
    df = pd.read_sql_query("select * from dbbikes_data where number = :number", conn, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)

    #generate means of the dublin bikes data per hours
    hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    df['update_hour'] = df.index.hour
    occupancy = df[['available_bike_stands', 'update_hour']].groupby('update_hour').mean()
    availability = df[['available_bikes', 'update_hour']].groupby('update_hour').mean()
    availability.index = hours
    occupancy.index = hours

    #generate means of dublin bikes data per day
    days = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    df['weekday'] = df.index.weekday
    mean_available_stands = df[['available_bike_stands', 'weekday']].groupby('weekday').mean()
    mean_available_bikes = df[['available_bikes', 'weekday']].groupby('weekday').mean()
    mean_available_stands.index = days
    mean_available_bikes.index = days

    #return result as json
    return jsonify(occupancy=occupancy.to_json(),
                   availability=availability.to_json(),
                   mean_available_stands=mean_available_stands.to_json(),
                   mean_available_bikes=mean_available_bikes.to_json()
                   )

if __name__ == "__main__":
    app.run(debug=True)
