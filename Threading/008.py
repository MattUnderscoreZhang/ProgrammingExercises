import threading
import queue
from time import sleep
import h5py as h5

class Threader():

    def __init__(self):
        self.my_queue = queue.Queue()
        self.count = 0
        self.my_threads = []
        for i in range(2):
            t = threading.Thread(target=self.work, args=(i,))
            t.start()
            self.my_threads.append(t)

    def work(self, do_file_load):
        while True:
            sleep(1)
            if do_file_load:
                for _ in range(50000):
                    data = h5.File("/Users/mattzhang/Dropbox/Projects/Data/test_h5.h5")
            self.count += 1
            self.my_queue.put(self.count)

    def __next__(self):
        value = self.my_queue.get()
        self.my_queue.task_done()
        return value

    def __iter__(self):
        return self

threader = Threader()
for data in threader:
    print(data)
