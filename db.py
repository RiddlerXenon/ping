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

            cur.execute(f"UPDATE pings set work_time = {work} WHERE work_start = '{row[1]}'")

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

    rows = cur.execute(f"SELECT * FROM pings WHERE user_ip = '{config.host}'")

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

    cur.execute(f"""
        UPDATE pings
        SET
            work_end = {int(time.time())},
            work_time = {int(time.time())} - (
                SELECT work_start
                FROM pings AS p
                WHERE
                    work_end IS NULL and pings.work_start = p.work_start
            )
        WHERE work_end IS NULL
    """)

    con.commit()
    con.close()