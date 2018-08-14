import threading

def test_function(a, b, c, d):
    print("Value is", (a+b+c)*d)

if __name__ == "__main__":
    for i in range(10):
        new_thread = threading.Thread(target=test_function, args=(i, 2, 3, i))
        new_thread.start()
