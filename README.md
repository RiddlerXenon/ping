*** УСТАНОВКА ***
В командной строке прописываем (на ПК должен быть устоновлен python):
  pip install -r requirements.txt

*** ЗАПУСК ***
В командной строке прописываем (на ПК должен быть устоновлен python):
  python3 main.py

*** ОПИСАНИЕ РАБОТЫ ПРОГРАММЫ ***

***
ФАЙЛ main.py
***
if __name__ == "__main__":
    main()
    
При запуске программы вызывается функция main()
***

***
def main():
    host = input("Input hostname: ") # host можно задать вручную
    # задаём хост, который будем пинговать

    signal.signal(signal.SIGINT, handler)
    # эта строчка отвечает для завершения программы без ошибок, для этого выполняется функция handler()

    do_schedule(host)
    # вызываем функцию do_schedule()
***
    
***
def handler(signum, frame):
  res = input("Ctrl-c was pressed. Do you really want to exit? y/n: ") спрашиваем нужно ли завешить программу

  if res == 'y': если да, то завершаем, иначе продолжаем работу
      config.time_end = int(time.time()) # В переменную конечного времени записываем настоящее время в формате Unix  

      db.work_time()
      вызываем функцию work_time() из файла db.py

      exit(1) 
***

***
def do_schedule(host):
    schedule.every(2).seconds.do(ping, host) # Запускаем функцию ping() каждые ...
                                             # Задаётся переодичность в секундах, по умолчанию 2 сек.
    
    # Запускаем бесконечный цикл для постоянного запуска предыдущей строчки
    while True:
        schedule.run_pending()
***

***
def ping(host):
    ping_rez = ping3.ping(host, unit='ms')
    # пингуем хост

    if ping_rez != None: если пинги идут
        if config.time_start == 0: # если стартовое время равно нулю, то задаём его текущим временем
            config.time_start = int(time.time()) # Время в формате Unix                                                    
        print(f"{ping_rez} ms")                  
                                                
    else: # если пингов нет, то задаём конечное время его текущим временем                                
        config.time_end = int(time.time()) # Время в формате Unix  
                                        
        db.work_time()
        # вызываем функцию work_time() из файла db.py

        print('Host not responding!')
***

***
ФАЙЛ db.py
***
def work_time():
    if config.time_start == 0: # если стартовое время равно нулю, то задаём его конечным временем
        config.time_start = config.time_end
            
    con = sql.connect('DB/pings.db') # Открываем файл с базой или создаём, если файла ещё нет
    work_time = config.time_end - config.time_start # вычисляет общее время работы

    with con: 
        cur = con.cursor() 

        cur.execute("CREATE TABLE IF NOT EXISTS 'pings' ('user_number' INTEGER PRIMARY KEY ASC, 'work_start' INTEGER, 'work_end' INTEGER, 'work_time' INTEGER)")
        # создаём таблицу в базе данных, если она ещё не создана
        
        cur.execute(f"INSERT INTO 'pings' ('work_start', 'work_end', 'work_time') VALUES ('{config.time_start}', '{config.time_end}', '{work_time}')")
        # записываем данные в базу данных
        
        con.commit()
        # сохраняем изменения
        
        cur.close()
        # закрываем базу

    config.time_end = 0 
    config.time_start = 0
    # обнуляем начальное и конечное время
***

***
ФАЙЛ config.py
***
time_start = 0
time_end = 0
# здесь записаны глобальные переменные для более уобного к ним обращения
***
