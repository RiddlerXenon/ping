import sqlite3 as sql

import time

import config

def work_time():
    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:
        if config.host == row[0] and row[1] is not None and row[2] is not None:
            work = row[2] - row[1]

            cur.execute(f"UPDATE pings set work_time = {work} WHERE user_ip = '{config.host}', work_start = '{row[1]}', work_end = '{row[2]}'")

    con.commit()
    con.close()

def end_time():
    count = 0

    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS pings (user_ip STRING, work_start INTEGER, work_end INTEGER, work_time INTEGER)")

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:
        if config.host == row[0] and row[1] is not None and row[2] is None:
            count += 1
            config.work_t = row[1]

    if count != 0:
        cur.execute(f"UPDATE pings set work_end = {int(time.time())} WHERE work_start = '{config.work_t}'")

    con.commit()
    con.close()

    work_time()

def start_time():
    count = 0

    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS pings (user_ip STRING, work_start INTEGER, work_end INTEGER, work_time INTEGER)")

    rows = cur.execute("SELECT user_ip, work_start, work_end FROM pings")

    for row in rows:
        if config.host == row[0] and row[1] is not None and row[2] is not None:
            count = 0
        elif config.host == row[0] and row[1] is not None and row[2] is None:
            count = 1

    if count == 0:
        cur.execute(f"INSERT INTO pings (user_ip, work_start) VALUES ('{config.host}', {int(time.time())})")

    con.commit()
    con.close()

def check():
    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS pings (user_ip STRING, work_start INTEGER, work_end INTEGER, work_time INTEGER)")

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:
        if row[1] is not None:
            con.close()

            end_time()

            break
    try: con.close() 
    except: pass

def finall():
    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:
        count = 0

        if row[1] is not None and row[2] is None:
            count += 1
            config.work_t = row[1]

        if count != 0:
            cur.execute(f"UPDATE pings set work_end = {int(time.time())} WHERE work_start = '{row[1]}'")
            cur.execute(f"UPDATE pings set work_time = {int(time.time()) - row[1]} WHERE work_start = '{row[1]}'")
    
    con.commit()
    con.close()