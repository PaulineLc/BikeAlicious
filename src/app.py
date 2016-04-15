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
    #for row in cur.execute("select * from dbbikes_data"):
        #print(row)
    return render_template('dublinbikes.html')

    
@app.route("/_station/<int:station_id>", methods= ['GET'])
def get_station_info(station_id):
    print("test!!")
    conn = get_db()
    df = pd.read_sql_query("select * from dbbikes_data where number = :number", conn, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    sample = '1h'
    occupancy = df['available_bike_stands'].resample(sample).mean()
    availability = df['available_bikes'].resample(sample).mean()

    days = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    df['weekday'] = df.index.weekday
    mean_available_stands = df[['available_bike_stands', 'weekday']].groupby('weekday').mean()
    mean_available_bikes = df[['available_bikes', 'weekday']].groupby('weekday').mean()
    mean_available_stands.index = days
    mean_available_bikes.index = days

    return jsonify(occupancy=occupancy.to_json(),
                   availability=availability.to_json(),
                   mean_available_stands=mean_available_stands.to_json(),
                   mean_available_bikes=mean_available_bikes.to_json()
                   )

    '''cur = get_db().cursor()

    #number of bike stand
    query = cur.execute("SELECT avg(bike_stands) FROM dbbikes_data WHERE number={}".format(number))
    number_stands = query.fetchone()[0]

    #station name
    query = cur.execute("SELECT name FROM dbbikes_data WHERE number={}".format(number))
    station_name = query.fetchone()[0]

    # number of bike stand
    query = cur.execute("SELECT avg(available_bike_stands) FROM dbbikes_data WHERE number={}".format(number))
    total_avg_empty_stands = query.fetchone()[0]

    # number of bike stand
    query = cur.execute("SELECT avg(available_bikes) FROM dbbikes_data WHERE number={}".format(number))
    total_avg_avail_bikes = query.fetchone()[0]

    #average monday
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('mon', number))
    avg_mon_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('mon', number))
    avg_mon_avail_bikes = query.fetchone()[0]

    #average tuesday
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('tue', number))
    avg_tue_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('tue', number))
    avg_tue_avail_bikes = query.fetchone()[0]

    #average wednesday
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('wed', number))
    avg_wed_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('wed', number))
    avg_wed_avail_bikes = query.fetchone()[0]

    #average Thu
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('thu', number))
    avg_thu_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('thu', number))
    avg_thu_avail_bikes = query.fetchone()[0]

    #average Fri
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('fri', number))
    avg_fri_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('fri', number))
    avg_fri_avail_bikes = query.fetchone()[0]

    #average Saturday
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('sat', number))
    avg_sat_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('sat', number))
    avg_sat_avail_bikes = query.fetchone()[0]

    #average Sunday
    query = cur.execute( "SELECT avg(available_bike_stands), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('sun', number))
    avg_sun_empty_stands = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes), case cast (strftime('%w', datetime(last_update/1000, 'unixepoch')) as integer) when 0 then 'sun' when 1 then 'mon' when 2 then 'tue' when 3 then 'wed' when 4 then 'thu' when 5 then 'fri' when 6 then 'sat' else '???' end as dayofweek FROM dbbikes_data WHERE dayofweek='{}' and number={}".format('sun', number))
    avg_sun_avail_bikes = query.fetchone()[0]

    #average midnight
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('00', number))
    avg_empty_stands_00 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('00', number))
    avg_avail_bikes_00 = query.fetchone()[0]

    #average 1am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('01', number))
    avg_empty_stands_01 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('01', number))
    avg_avail_bikes_01 = query.fetchone()[0]

    #average 2am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('02', number))
    avg_empty_stands_02 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('02', number))
    avg_avail_bikes_02 = query.fetchone()[0]

    #average 3am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('03', number))
    avg_empty_stands_03 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('03', number))
    avg_avail_bikes_03 = query.fetchone()[0]

    #average 4am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('04', number))
    avg_empty_stands_04 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('04', number))
    avg_avail_bikes_04 = query.fetchone()[0]

    #average 5am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('05', number))
    avg_empty_stands_05 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('05', number))
    avg_avail_bikes_05 = query.fetchone()[0]


    #average 6am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('06', number))
    avg_empty_stands_06 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('06', number))
    avg_avail_bikes_06 = query.fetchone()[0]

    #average 7am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('07', number))
    avg_empty_stands_07 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('07', number))
    avg_avail_bikes_07 = query.fetchone()[0]

    #average 8am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('08', number))
    avg_empty_stands_08 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('08', number))
    avg_avail_bikes_08 = query.fetchone()[0]

    #average 9am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('09', number))
    avg_empty_stands_09 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('09', number))
    avg_avail_bikes_09 = query.fetchone()[0]

    #average 10am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('10', number))
    avg_empty_stands_10 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('10', number))
    avg_avail_bikes_10 = query.fetchone()[0]

    #average 11am
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('11', number))
    avg_empty_stands_11 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('11', number))
    avg_avail_bikes_11 = query.fetchone()[0]

    #average noon
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('12', number))
    avg_empty_stands_12 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('12', number))
    avg_avail_bikes_12 = query.fetchone()[0]

    #average 1pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('13', number))
    avg_empty_stands_13 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('13', number))
    avg_avail_bikes_13 = query.fetchone()[0]

    #average 2pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('14', number))
    avg_empty_stands_14 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('14', number))
    avg_avail_bikes_14 = query.fetchone()[0]

    #average 3pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('15', number))
    avg_empty_stands_15 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('15', number))
    avg_avail_bikes_15 = query.fetchone()[0]

    #average 4pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('16', number))
    avg_empty_stands_16 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('16', number))
    avg_avail_bikes_16 = query.fetchone()[0]

    #average 5pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('17', number))
    avg_empty_stands_17 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('17', number))
    avg_avail_bikes_17 = query.fetchone()[0]

    #average 6pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('18', number))
    avg_empty_stands_18 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('18', number))
    avg_avail_bikes_18 = query.fetchone()[0]

    #average 7pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('19', number))
    avg_empty_stands_19 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('19', number))
    avg_avail_bikes_19 = query.fetchone()[0]

    #average 8pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('20', number))
    avg_empty_stands_20 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('20', number))
    avg_avail_bikes_20 = query.fetchone()[0]

    #average 9pn
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('21', number))
    avg_empty_stands_21 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('21', number))
    avg_avail_bikes_21 = query.fetchone()[0]

    #average 10pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('22', number))
    avg_empty_stands_22 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('22', number))
    avg_avail_bikes_22 = query.fetchone()[0]

    #average 11pm
    query = cur.execute( "SELECT avg(available_bike_stands) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('23', number))
    avg_empty_stands_23 = query.fetchone()[0]
    query = cur.execute( "SELECT avg(available_bikes) FROM dbbikes_data WHERE strftime('%H', datetime(last_update/1000, 'unixepoch'))='{}' and number={}".format('23', number))
    avg_avail_bikes_23 = query.fetchone()[0]


    return jsonify(number = number,
                   number_stands = number_stands,
                   station_name = station_name,
                   total_avg_avail_bikes = total_avg_avail_bikes,
                   total_avg_empty_stands = total_avg_empty_stands,
                   avg_mon_empty_stands = avg_mon_empty_stands,
                   avg_mon_avail_bikes = avg_mon_avail_bikes,
                   avg_tue_empty_stands = avg_tue_empty_stands,
                   avg_tue_avail_bikes = avg_tue_avail_bikes,
                   avg_wed_empty_stands=avg_wed_empty_stands,
                   avg_wed_avail_bikes=avg_wed_avail_bikes,
                   avg_thu_empty_stands=avg_thu_empty_stands,
                   avg_thu_avail_bikes=avg_thu_avail_bikes,
                   avg_fri_empty_stands=avg_fri_empty_stands,
                   avg_fri_avail_bikes=avg_fri_avail_bikes,
                   avg_sat_empty_stands=avg_sat_empty_stands,
                   avg_sat_avail_bikes=avg_sat_avail_bikes,
                   avg_sun_empty_stands=avg_sun_empty_stands,
                   avg_sun_avail_bikes=avg_sun_avail_bikes,
                   avg_empty_stands_00 = avg_empty_stands_00,
                   avg_avail_bikes_00 = avg_avail_bikes_00,
                   avg_empty_stands_01=avg_empty_stands_01,
                   avg_avail_bikes_01=avg_avail_bikes_01,
                   avg_empty_stands_02=avg_empty_stands_02,
                   avg_avail_bikes_02=avg_avail_bikes_02,
                   avg_empty_stands_03=avg_empty_stands_03,
                   avg_avail_bikes_03=avg_avail_bikes_03,
                   avg_empty_stands_04=avg_empty_stands_04,
                   avg_avail_bikes_04=avg_avail_bikes_04,
                   avg_empty_stands_05=avg_empty_stands_05,
                   avg_avail_bikes_05=avg_avail_bikes_05,
                   avg_empty_stands_06=avg_empty_stands_06,
                   avg_avail_bikes_06=avg_avail_bikes_06,
                   avg_empty_stands_07=avg_empty_stands_07,
                   avg_avail_bikes_07=avg_avail_bikes_07,
                   avg_empty_stands_08=avg_empty_stands_08,
                   avg_avail_bikes_08=avg_avail_bikes_08,
                   avg_empty_stands_09=avg_empty_stands_09,
                   avg_avail_bikes_09=avg_avail_bikes_09,
                   avg_empty_stands_10=avg_empty_stands_10,
                   avg_avail_bikes_10=avg_avail_bikes_10,
                   avg_empty_stands_11=avg_empty_stands_11,
                   avg_avail_bikes_11=avg_avail_bikes_11,
                   avg_empty_stands_12=avg_empty_stands_12,
                   avg_avail_bikes_12=avg_avail_bikes_12,
                   avg_empty_stands_13=avg_empty_stands_13,
                   avg_avail_bikes_13=avg_avail_bikes_13,
                   avg_empty_stands_14=avg_empty_stands_14,
                   avg_avail_bikes_14=avg_avail_bikes_14,
                   avg_empty_stands_15=avg_empty_stands_15,
                   avg_avail_bikes_15=avg_avail_bikes_15,
                   avg_empty_stands_16=avg_empty_stands_16,
                   avg_avail_bikes_16=avg_avail_bikes_16,
                   avg_empty_stands_17=avg_empty_stands_17,
                   avg_avail_bikes_17=avg_avail_bikes_17,
                   avg_empty_stands_18=avg_empty_stands_18,
                   avg_avail_bikes_18=avg_avail_bikes_18,
                   avg_empty_stands_19=avg_empty_stands_19,
                   avg_avail_bikes_19=avg_avail_bikes_19,
                   avg_empty_stands_20=avg_empty_stands_20,
                   avg_avail_bikes_20=avg_avail_bikes_20,
                   avg_empty_stands_21=avg_empty_stands_21,
                   avg_avail_bikes_21=avg_avail_bikes_21,
                   avg_empty_stands_22=avg_empty_stands_22,
                   avg_avail_bikes_22=avg_avail_bikes_22,
                   avg_empty_stands_23=avg_empty_stands_23,
                   avg_avail_bikes_23=avg_avail_bikes_23
                   )'''

if __name__ == "__main__":
    app.run(debug=True)
