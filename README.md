### УСТАНОВКА ###
В командной строке прописываем (на ПК должен быть устоновлен python):
  ```
  pip install -r requirements.txt
  ```

### ЗАПУСК ###
В командной строке прописываем (на ПК должен быть устоновлен python):
  ```
  python3 main.py
  ```

### ОПИСАНИЕ РАБОТЫ ПРОГРАММЫ ###

*** ФАЙЛ main.py ***

  ```
  def main():
    host = input("Input hostname: ")        # Задание хоста в формате 192.168.0.0
    mask = input("Input the subnet mask: ") # Задание маски в формате 255.255.255.0

    signal.signal(signal.SIGINT, handler)   # Обращение к функции handler при закрытии скрипта через Ctrl+C

    calc.mask_calc(host, mask)              # Обращение к функции mask_calc в файле calc.py

  ```

  ```

  def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n: ") # Запрашиваем нужно ли закрывать скрипт

    if res == 'y':                                                       # Если да, то
        db.finall()                                                      # обращаемся к функции finall в файле db.py
            
        exit(1)                                                          # Закрываем скрипт

  ```

  ```

  def ping(hosts):
    for i in hosts:                            # Запускаем цикл перебора ip в маске
        ping_rez = ping3.ping(i, unit='ms')    # Пингуем ip
        config.host = i                        # Записываем ip в переменную host в файле config.py

        # print(ping_rez)                              # Вывод пинга
        if ping_rez != None and ping_rez != False:     # Если пинг не проходит, то
            db.start_time()                            # обращаемся к функции start_time в файле db.py
        else:                                          # иначе
            db.check()                                 # обращаемся к функции check в файле db.py

  ```

  ```

  def do_schedule(hosts):
    ping(hosts)                                # Выполняем функцию ping

    schedule.every(5).minutes.do(ping, hosts)  # Выполнение функции ping каждые 5 минут (можно поменять)

    while True:                                # Запускаем бесконечный цикл,
        schedule.run_pending()                 # который будет поддерживать работоспособность таймера

  ```

  ```

  if __name__ == "__main__": # Только если запущен файл main.py,
    main()                   # выполняем функцию main

  ```

*** ФАЙЛ calc.py ***

  ```

  def mask_calc(ip, mask):
    net = IPv4Network((ip, mask))       # Получаем ip адреса из маски
    hosts = list(net.hosts())           # создаём список адресов сети

    main.do_schedule(dl, hosts)         # Обращаемся к функции do_schedule в файле main.py

  ```

*** ФАЙЛ db.py ***

  ```

  def work_time():
    con = sql.connect('DB/pings.db')            # Подключение к базе данных
    cur = con.cursor()                          # определение курсора в базе

    rows = cur.execute("SELECT * FROM pings")   # выбор всех данных

    for row in rows:                                                            # Производим перебор по каждой строке таблицы
        if config.host == row[0] and row[1] is not None and row[2] is not None: # если у устройства есть время начала работы и время конца
            work = row[2] - row[1]                                              # вычисляем общее время работы

            cur.execute(f"UPDATE pings set work_time = {work} WHERE user_ip = '{config.host}', work_start = '{row[1]}', work_end = '{row[2]}'") # Заносим общее время работы в базу

    con.commit() # Сохраняем изменения
    con.close()  # Закрываем базу

  ```

(Большинство действий в последующих функциях будут анологичными, поэтому я не буду их комментировать)

  ```

  def end_time():
    count = 0     # Задаём локальную переменную count

    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS pings (user_ip STRING, work_start INTEGER, work_end INTEGER, work_time INTEGER)") # Создаём базу если её не сущестует

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:
        if config.host == row[0] and row[1] is not None and row[2] is None:
            count += 1
            config.work_t = row[1]

    if count != 0:
        cur.execute(f"UPDATE pings set work_end = {int(time.time())} WHERE work_start = '{config.work_t}'")  # Задаём время окончания работы

    con.commit()
    con.close()

    work_time()

  ```

  ```

  def start_time():
    count = 0

    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS pings (user_ip STRING, work_start INTEGER, work_end INTEGER, work_time INTEGER)")

    rows = cur.execute("SELECT user_ip, work_start, work_end FROM pings")

    for row in rows:
        if config.host == row[0] and row[1] is not None and row[2] is not None: # Если устройво уже есть в базе, но начальное и конечное времена уже заданы
            count = 0                                                           # приравниваем count к нулю
        elif config.host == row[0] and row[1] is not None and row[2] is None:   # Если устройво уже есть в базе, но задано только начальное время
            count = 1                                                           # приравниваем count к единице

    if count == 0:                                                                                           # Если count равен нулю
        cur.execute(f"INSERT INTO pings (user_ip, work_start) VALUES ('{config.host}', {int(time.time())})") # Задаём начальное время

    con.commit()
    con.close()

  ```

  ```

  def check():
    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS pings (user_ip STRING, work_start INTEGER, work_end INTEGER, work_time INTEGER)")

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:            
        if row[1] is not None:   # Если время начал работы существует
            con.close()

            end_time()           # обращаемся к функции end_time

            break
    try: con.close() 
    except: pass

  ```

  ```

  def finall():
    con = sql.connect('DB/pings.db')
    cur = con.cursor()

    rows = cur.execute("SELECT * FROM pings")

    for row in rows:                                     # Здесь производится проверка всех уствойств в базе
        count = 0                                        # для них задаётся конечное время работы
                                                         # и вычисляется общее время работы
        if row[1] is not None and row[2] is None:
            count += 1
            config.work_t = row[1]

        if count != 0:
            cur.execute(f"UPDATE pings set work_end = {int(time.time())} WHERE work_start = '{row[1]}'")
            cur.execute(f"UPDATE pings set work_time = {int(time.time()) - row[1]} WHERE work_start = '{row[1]}'")
    
    con.commit()
    con.close()

  ```