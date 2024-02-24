import threading, time

def sleepsort(int_list: int, duration: float):
    max_value = int_list[0]
    min_value = int_list[0]

    for i in int_list:
        max_value = max(max_value, i)
        min_value = min(min_value, i)

    start = [False]

    time_variance = (duration-0.1)/max_value
    sorted_list = []
    threads = []

    for i in int_list:
        threads.append(threading.Thread(target=sleepcode, args=[sorted_list, start, time_variance*i, i]))

    for thread in threads:
        thread.start()

    start[0] = True
    time.sleep(duration)
    return sorted_list

def sleepcode(int_list: list, start: bool, sleep_time: int, value:int):
    while not start[0]:
        pass
    time.sleep(sleep_time)
    int_list.append(value)

if __name__ == '__main__':
    print('Hello World!')
    a = time.time()
    print(sleepsort([i for i in range(10,0,-1)],.101))
    print(time.time()-a)

    b = time.time()
    sorted([i for i in range(10,0,-1)])
    print(time.time()-b)
