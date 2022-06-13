blah = [1, 2, 3, 4, 5]


def get_next():
    for i in blah:
        yield i


if __name__ == "__main__":
    for i in get_next():
        print(i)
        if i == 4:
            break
