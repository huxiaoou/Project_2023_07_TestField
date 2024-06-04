import os
import multiprocessing
import time


def write_file():
    print(os.getpid(), os.getppid())
    lock.acquire()
    with open('./2.log', 'a') as f:
        f.write("xxxx")
    lock.release()


def init_lock(lk):
    global lock
    lock = lk


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    pool = multiprocessing.Pool(processes=5, initializer=init_lock, initargs=(lock,))
    for i in range(5):
        handler = pool.apply_async(write_file)
        print(handler.get())
