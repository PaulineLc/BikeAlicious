from src.data_scrapping import neatify_coord
import os.path
import sqlite3

#test database creation
def test_db_creation():
    dummy_db = 'dummy_db.db' #update to whatever database you want to create, if required
    conn = sqlite3.connect(dummy_db)
    assert(os.path.isfile(dummy_db))

test_db_creation()

#test database table creation
def test_db_table_creation():
    dummy_db = 'dummy_db.db' #update to whatever database you want to create a table in, if required
    conn = sqlite3.connect(dummy_db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE dummy_data(integer_test INT, text_test TEXT, float_test REAL)")
    results = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    assert(cur.fetchone()[0] == 'dummy_data')

test_db_table_creation()

#test database table insertion
def test_db_table_insertion():
    dummy_db = 'dummy_db.db' #update to whatever database test, if required
    conn = sqlite3.connect(dummy_db)
    cur = conn.cursor()
    cur.execute("INSERT INTO dummy_data VALUES(?, ?, ?)", (1,"test",1.0))
    results = cur.execute("SELECT * FROM dummy_data")
    assert(cur.fetchone() == (1, 'test', 1.0))

test_db_table_insertion()

#test database illegal insertion
def test_db_table_illegal_insertion():
    dummy_db = 'dummy_db.db' #update to whatever database test, if required
    conn = sqlite3.connect(dummy_db)
    cur = conn.cursor()
    cur.execute("INSERT INTO dummy_data VALUES(?, ?, ?)", (1.23, 1000,"test"))
    results = cur.execute("SELECT * FROM dummy_data")
    print(cur.fetchall())
    #This works anyway because SQLite is not stringly typed
    #http://dba.stackexchange.com/questions/106364/text-string-stored-in-sqlite-integer-column
    #Hence, we decided to force value check in our live code by casting all expected integer values to integers.

test_db_table_illegal_insertion()

#test database illegal insertion by checking values
def test_db_table_illegal_insertion_cast():
    dummy_db = 'dummy_db.db' #update to whatever database test, if required
    conn = sqlite3.connect(dummy_db)
    cur = conn.cursor()
    illegal_insertion_1 = int(1.23) #will cast to int
    illegal_insertion_2 = int("test") #will not cast to int
    cur.execute("INSERT INTO dummy_data VALUES(?, ?, ?)", (illegal_insertion_1, illegal_insertion_2,"test"))
    results = cur.execute("SELECT * FROM dummy_data")
    print(cur.fetchall())
    #This works anyway because SQLite is not stringly typed
    #http://dba.stackexchange.com/questions/106364/text-string-stored-in-sqlite-integer-column
    #Hence, we decided to force value check in our live code by casting all expected integer values to integers.

#test_db_table_illegal_insertion_cast() #error expected here

#test the trimming of the data, also as a way to check what data is input in the database
def test_neatify_coord():
    test_string1 = "{[123.123,][}}}"
    test_string2 = "123.123,][}}}"
    test_string3 = "{[123.123"
    assert(neatify_coord(test_string1) == 123.123)
    assert(neatify_coord(test_string2) == 123.123)
    assert(neatify_coord(test_string3) == 123.123)

test_neatify_coord()