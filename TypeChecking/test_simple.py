def subtract(x: int, y: int) -> int:
    return x - y


def test_subtract():
    subtract(3, "dsf")
    assert(subtract(3, 6) == -3)


# "mypy test_types.py" or "\mp" in vim
test_subtract()
subtract(3, "dsf")  # should throw an error
