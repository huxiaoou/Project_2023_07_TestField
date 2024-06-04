import os
import multiprocessing
import time


def write_file(lock):
    print(os.getpid(), os.getppid())
    lock.acquire()
    with open('./t.log', 'a') as f:
        f.write("\nbbb")
    lock.release()


if __name__ == '__main__':
    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes=5)
    for i in range(5):
        handler = pool.apply_async(write_file, (lock, ))
        # print(handler.get())
    # try:
    #     while True:
    #         time.sleep(3600)
    #         continue
    # except KeyboardInterrupt:
    #     pool.close()
    #     pool.join()
    pool.close()
    pool.join()
