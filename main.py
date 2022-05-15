import schedule

import signal

import ping3

import time

import config

import db

import calc

def main():
    host = input("Input hostname: ")
    mask = input("Input the subnet mask: ")

    signal.signal(signal.SIGINT, handler)

    calc.mask_calc(host, mask)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n: ")

    if res == 'y':          
        db.finall()

        exit(1)

def ping(hosts):
    for i in hosts:
        ping_rez = ping3.ping(str(i), unit='ms')
        config.host = str(i)

        # print(ping_rez, '\n', i)
        if ping_rez != None and ping_rez != False:
            db.start_time()                                               
        else:                                
            db.check()

def do_schedule(hosts):
    config.t_s = int(time.time())

    ping(hosts)

    config.t_e = int(time.time())

    schedule.every(((config.t_e - config.t_s) // 60) + 2).minutes.do(ping, hosts)

    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()