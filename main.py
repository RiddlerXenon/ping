import sqlite3 as sql

import schedule

import signal

import ping3

import config

import db

import calc

def main():
    host = input("Input hostname: ") # host можно задать вручную
    mask = input("Input the subnet mask: ")

    signal.signal(signal.SIGINT, handler)

    calc.mask_calc(host, mask)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n: ")

    if res == 'y':          
        db.finall()
            
        exit(1)

def ping(host, fr, to):
    for i in range(fr, to):
        ping_rez = ping3.ping(f'{host}{i}', unit='ms')
        config.host = f'{host}{i}'

        print(ping_rez)
        if ping_rez != None and ping_rez != False:
            db.start_time()                                               
        else:                                
            db.check()

def do_schedule(host, fr, to):
    ping(host, fr, to)

    schedule.every(2).minutes.do(ping, host, fr, to)

    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()