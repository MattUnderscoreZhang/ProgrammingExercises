from typing import NewType


Name = NewType("Name", str)
bella = Name("Bella")


def print_name(name: Name) -> None:
    print(name)


def print_string(string: str) -> None:
    print(string)


print_name(bella)
print_string(bella)
