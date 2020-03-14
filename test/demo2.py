#######################################################################################
# Param Data @
# Return @
# TODO @ 使用队列进行线程之间通信
# *
# !
# ?
#######################################################################################
from threading import Thread, Event
from queue import Queue
import time
import random

# 生产者

# 这里直接可以将线程类通过参数传递进来,不用单独创建了
class producer(Thread):
    def __init__(self, queue):
        # 这里必须调用init初始化方法
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(10):

            item = random.randint(0, 256)
            # 向queue  put数据
            self.queue.put(item)
            print('Producer notify: item N° %d appended to queue by %s' %
                  (item, self.name))
            time.sleep(1)


class consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # 消费数据
            item = self.queue.get()
            print('Consumer notify : %d popped from queue by %s' %
                  (item, self.name))
            self.queue.task_done()


def main():
    queue = Queue()
    # 一个生产者3个消费者
    t1 = producer(queue)
    t2 = consumer(queue)
    t3 = consumer(queue)
    t4 = consumer(queue)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()


if __name__ == '__main__':
    main()
