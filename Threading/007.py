import threading
import queue
from time import sleep

class Threader():

    def __init__(self):
        self.my_queue = queue.Queue()
        self.count = 0
        self.my_threads = []
        for _ in range(4):
            t = threading.Thread(target=self.work)
            t.start()
            self.my_threads.append(t)

    def work(self):
        while True:
            sleep(1)
            self.count += 1
            self.my_queue.put(self.count)

    def queue_reader(self):
        while True:
            value = self.my_queue.get()
            yield value
            self.my_queue.task_done()

threader = Threader()
for data in threader.queue_reader():
    print(data)
