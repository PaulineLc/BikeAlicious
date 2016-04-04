from flask import Flask
from flask import g
import sqlite3

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
    for row in cur.execute("select * from dbbikes_data"):
        print(row)
    return "Hellow World!"

    
@app.route("/station/<int:number>")
def get_station_info(number):
    return "Fetching info for {}".format(number)

if __name__ == "__main__":
    app.run(debug=True)