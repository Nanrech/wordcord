ass = {"c": 1,
       "loo": {
           "woo": 8,
           "kill": {
               "meer": 1,
               "kat": 3
           }
       }}
# print(len(ass), len(ass["loo"]), ass["loo"]["kill"])

import sqlite3

# DB stuff!
conn = sqlite3.connect('../resources/userbase.db')
c = conn.cursor()


def _create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')


def _data_entry():
    c.execute("INSERT INTO stuffToPlot VALUES(86754865, '2016-01-01', 'Python', 8)")
    conn.commit()
    c.close()
    conn.close()


_create_table()
_data_entry()
