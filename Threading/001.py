import threading

def test_function():
    print("Testing")

if __name__ == "__main__":
    for _ in range(10):
        new_thread = threading.Thread(target=test_function)
        new_thread.start()
