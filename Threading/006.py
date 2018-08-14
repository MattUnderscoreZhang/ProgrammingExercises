import threading
import queue
from time import sleep

my_queue = queue.Queue()
count = 0

def work():
    global count
    while True:
        sleep(1)
        count += 1
        my_queue.put(count)

my_threads = []
for _ in range(4):
    t = threading.Thread(target=work)
    t.start()
    my_threads.append(t)

def queue_reader():
    while True:
        value = my_queue.get()
        yield value
        my_queue.task_done()

for data in queue_reader():
    print(data)
