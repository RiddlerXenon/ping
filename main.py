import schedule

import signal

import ping3

import time

import config

import db

def main():
    host = input("Input hostname: ") # host можно задать вручную

    signal.signal(signal.SIGINT, handler)

    do_schedule(host)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n: ")

    if res == 'y':
        if config.time_start == 0:    
            exit(1)
        else:
            config.time_end = int(time.time()) # Время в формате Unix  
                                            
            db.work_time()
            
            exit(1)

def ping(host):
    ping_rez = ping3.ping(host, unit='ms')

    if ping_rez != None and ping_rez != False:
        if config.time_start == 0:
            config.time_start = int(time.time()) # Время в формате Unix                                                    
        print(f"{ping_rez} ms")                  
                                                
    else:       
        if config.time_start == 0:    
            print('Host not responding!')
        else:
            config.time_end = int(time.time()) # Время в формате Unix  
                                            
            db.work_time()

            print('Host not responding!')

def do_schedule(host):
    schedule.every(2).seconds.do(ping, host) # Задание переодичности в секундах, по умолчанию 2 сек.

    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()