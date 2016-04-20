Dublin Bikes Occupancy Map
========================================

Overview
--------

The aim of this website is to show the occupancy of Dublin Bikes stations (current occupancy as well as historic average).

Requirements
------------

This program uses Python 3 and the following librairies:
- flask
- sqlite3
- pandas

How to use
------------

Open a terminal and cd to the directory where you have extracted the files. Then, execute the following commands:

if your default Python is Python 3:

```bash
cd src
python app.py
```
or, if your default Python is Python 2:

```bash
cd src
python3 app.py
```

Using your favorite browser, please visit 127.0.0.1:5000 to see the website.

Technical notes
-------------

Our Git repositories is available at: https://git.ucd.ie/Pauline/dublin-bikes-group-project

The test folder contains some tests to make sure our program behaves correctly

data_scrapping.py is the program querying the JCDecaux website, and update the database. You should not need to launch it to use our website.

app.py largely relies on Flask, and renders the website.
