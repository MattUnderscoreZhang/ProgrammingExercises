import threading
import logging

# level = lowest reporting level
# keywords list here: http://www.bogotobogo.com/python/Multithread/python_multithreading_Identify_Naming_Logging_threads.php
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-9s) %(message)s')

def test_function(id):
    logging.debug("ID of thread " + threading.currentThread().getName() + " is " + str(id))

if __name__ == "__main__":
    names = ['Allan', 'Bean', 'Carlie', 'Denver', 'Eowin', 'Francis', 'Georgina', 'Hector', 'Iocasus', 'Joana']
    threads = []
    for i in range(10):
        threads.append(threading.Thread(name=names[i], target=test_function, args=(i,)))
    for i in range(10):
        threads[i].start()
