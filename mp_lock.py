import multiprocessing
import time


def task1(lock):
    with lock:  # with上下文语句使用锁，会自动释放锁
        n = 5
        while n > 1:
            print(f"{time.strftime('%H:%M:%S')} task1 输出信息")
            time.sleep(1)
            n -= 1


def task2(lock):
    lock.acquire()
    n = 5
    while n > 1:
        print(f"{time.strftime('%H:%M:%S')} task2 输出信息")
        time.sleep(1)
        n -= 1
    lock.release()


def task3(lock):
    lock.acquire()
    n = 5
    while n > 1:
        print(f"{time.strftime('%H:%M:%S')} task3 输出信息")
        time.sleep(1)
        n -= 1
    lock.release()


if __name__ == "__main__":
    lock = multiprocessing.Lock()
    p1 = multiprocessing.Process(target=task1, args=(lock,))
    p2 = multiprocessing.Process(target=task2, args=(lock,))
    p3 = multiprocessing.Process(target=task3, args=(lock,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
