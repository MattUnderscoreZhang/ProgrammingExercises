import threading

def test_function(id):
    print("ID is", id)

if __name__ == "__main__":
    for i in range(10):
        new_thread = threading.Thread(target=test_function, args=(i,))
        new_thread.start()
