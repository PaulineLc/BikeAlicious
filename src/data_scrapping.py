'''
Created on 8 Mar 2016

@author: pauline
'''

import json
import sqlite3 as lite
from time import sleep
import requests


master_db = lite.connect('dbike_masterDB_test.db')

name = "dublin"
stations = "https://api.jcdecaux.com/vls/v1/stations"
apikey = "18115ec8d21d6ab03e40cf69eac0fc48e613f3bd"

json_file = requests.get(stations, params={"apiKey": apikey, "contract" : name})
parsed_json_file = json.loads(json_file.text)


while True:
    try:
        with master_db:
            
            cursor_db = master_db.cursor()
            
            try:
                cursor_db.execute('CREATE TABLE dbbikes_data(number INT, name TEXT, address TEXT, latitude REAL, longitude REAL, banking INT, bonus INT, status TEXT, contract_name TEXT, bike_stands INT, available_bike_stands INT, available_bikes INT, last_update REAL)')
            except:
                pass
            
            for line in range(len(parsed_json_file)):
                number = parsed_json_file[line]['number']
                number = int(number)
                name = parsed_json_file[line]['name']
                address = parsed_json_file[line]['address']
                coord = parsed_json_file[line]['position']
                coord = str(coord).split(" ")
                latitude = coord[1]
                latitude = latitude.replace(",", "")
                latitude = float(latitude)
                longitude = coord[3]
                longitude = longitude.replace("}", "")
                longitude = longitude.replace("]", "")
                longitude = float(longitude)
                banking = parsed_json_file[line]['banking']
                banking = int(banking)
                bonus = parsed_json_file[line]['bonus']
                bonus = int(bonus)
                status = parsed_json_file[line]['status']
                contract_name = parsed_json_file[line]['contract_name']
                bike_stands = parsed_json_file[line]['bike_stands']
                bike_stands = int(bike_stands)
                available_bike_stands = parsed_json_file[line]['available_bike_stands']
                available_bike_stands = int(available_bike_stands)
                available_bikes = parsed_json_file[line]['available_bikes']
                available_bikes = int(available_bikes)
                last_update = parsed_json_file[line]['last_update']
                last_update = float(last_update)
                cursor_db.execute("INSERT INTO dbbikes_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" , (number, name, address, latitude, longitude, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update))
    
                def writedata(data):
                    f = open('Test_masterdb.sql', 'w')
                    with f:
                        f.write(data)
                
                writedata('\n'.join(master_db.iterdump()))
                
        sleep(5 * 60)

    except:
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        sleep(5)