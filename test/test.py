import threading

# 共享资源
l = 0
# 加锁
lock = threading.Lock()


def task_add1():
    global l
    # 改成100w线程不安全的效果出来了
    for i in range(1000000):
        # lock.acquire()
        l += 1
        # lock.release()


def task_add2():

    global l
    for i in range(1000000):
        # lock.acquire()
        l -= 1

        # lock.release()


def run():
    # 可以给线程命名
    t1 = threading.Thread(name="t1", target=task_add1)
    t2 = threading.Thread(name="t2", target=task_add2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def main():
    run()
    print(l)


if __name__ == '__main__':
    main()
