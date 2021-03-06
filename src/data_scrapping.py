import json
import sqlite3 as lite
from time import sleep
import requests
import traceback


def writedata(data, sql_file_name):
        '''write data to database'''
        f = open(sql_file_name, 'w')
        with f:
            f.write(data)

def neatify_coord(string):
    '''trim input from the dublin bikes json'''
    neat_string = ""
    
    for i in range(len(string)):
        if not string[i].isnumeric():
            neat_string = string[i+1:]
        else:
            break
        
    if neat_string == "":
        neat_string = string
    else:
        string = neat_string

    for i in range(len(string) - 1, 0, -1):
        if not string[i].isnumeric():
            neat_string = string[:i]
        else:
            break
        
    neat_string = float(neat_string)
    return neat_string
    
def launch_database():
    '''lauches the database'''
    master_db = lite.connect('dbike_masterDB_test.db')
    
    contract = "dublin"
    stations = "https://api.jcdecaux.com/vls/v1/stations"
    apikey = "18115ec8d21d6ab03e40cf69eac0fc48e613f3bd"

    while True:
        
        try:
            
            '''get data from jcdecaux'''
            json_file = requests.get(stations, params={"apiKey": apikey, "contract" : contract})
            parsed_json_file = json.loads(json_file.text)
            
            json__current_data = open('json_current_data.json', 'w')
            json__current_data.write(json_file.text)
            json__current_data.close()

            with master_db:
                '''open database connection'''
                cursor_db = master_db.cursor()
                
                try:
                    '''if table doesn't yet exist, creates it'''
                    cursor_db.execute('CREATE TABLE dbbikes_data(number INT, name TEXT, address TEXT, latitude REAL, longitude REAL, banking INT, bonus INT, status TEXT, contract_name TEXT, bike_stands INT, available_bike_stands INT, available_bikes INT, last_update INT)')
                except lite.OperationalError as e:
                        if e == "table Test dbbikes_data exists":
                            pass
                
                '''adds fected data to database'''
                for line in range(len(parsed_json_file)):
                    number = parsed_json_file[line]['number']
                    number = int(number)
                    name = parsed_json_file[line]['name']
                    address = parsed_json_file[line]['address']
                    coord = parsed_json_file[line]['position']
                    coord = str(coord).split(" ")
                    latitude = coord[1]
                    latitude = neatify_coord(latitude)
                    longitude = coord[3]
                    longitude = neatify_coord(longitude)
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
                    last_update = int(last_update)
                    cursor_db.execute("INSERT INTO dbbikes_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" , (number, name, address, latitude, longitude, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update))
            
            '''transforms sqlite database to sql database'''
            '''we didn't actually used it - we created for convenience'''
            writedata('\n'.join(master_db.iterdump()), 'Test_masterdb.sql')
            sleep(60 * 5)
    
        except:
            print(":-(")
            print(traceback.format_exc())
            sleep(5)

#uncomment the below to run the database
#launch_database()
