import threading

def test_function(id):
    print("ID of thread", threading.currentThread().getName(), "is", id)

if __name__ == "__main__":
    names = ['Allan', 'Bean', 'Carlie', 'Denver', 'Eowin', 'Francis', 'Georgina', 'Hector', 'Iocasus', 'Joana']
    threads = []
    for i in range(10):
        threads.append(threading.Thread(name=names[i], target=test_function, args=(i,)))
    for i in range(10):
        threads[i].start()
