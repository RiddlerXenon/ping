import sqlite3 as sql

import config

def work_time():
    con = sql.connect('DB/pings.db')
    work_time = config.time_end - config.time_start

    with con:
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS 'pings' ('user_number' INTEGER PRIMARY KEY ASC, 'work_start' INTEGER, 'work_end' INTEGER, 'work_time' INTEGER)")

        cur.execute(f"INSERT INTO 'pings' ('work_start', 'work_end', 'work_time') VALUES ('{config.time_start}', '{config.time_end}', '{work_time}')")

        con.commit()
        cur.close()

    config.time_end = 0
    config.time_start = 0