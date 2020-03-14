#######################################################################################
# Param Data @
# Return @
# TODO @ 信号量进行线程同步,信号量是操作系统内部管理的抽象数据
# TODO @ 本质上信号量是内部数据, 用于标明当前的共享资源有多少并发读取
# *
# !
# ?
#######################################################################################

# 获取会减少信号量的内部变量,当信号量是负值的时候线程会被挂起,直到有其他线程释放资源
# 当线程不再需要该共享资源，必须通过 release() 释放。这样，信号量的内部变量增加，在信号量等待队列中排在最前面的线程会拿到共享资源的权限。

# 信号量是原子的并没有什么问题, 如果不是或者两个操作有一个终止就会导致情况槽糕
# 可以用with的语法管理 信号量，条件变量，事件和锁
# 但是更常见的方式是队列
import threading
import logging


lock = threading.Lock()
rlock = threading.RLock()
condition = threading.Condition()
mutex = threading.Semaphore(1)
threading_synchronization_list = [lock, rlock, condition, mutex]


def threading_with(statement):
    with statement:
        logging.debug('%s acquired via with' % statement)


def threading_not_with(statement):
    statement.acquire()
    try:
        logging.debug('%s acquired directly' % statement)
    finally:
        statement.release()


for statement in threading_synchronization_list:
    t1 = threading.Thread(target=threading_with, args=(statement,))
    t2 = threading.Thread(target=threading_not_with, args=(statement,))
