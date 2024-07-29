from jinja2 import Environment, FileSystemLoader


max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75},
]


def print_messages():
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("message.txt")


    for student in students:
        content = template.render(
            student,
            max_score=max_score,
            test_name=test_name
        )
        print(content)
        print("\n=============\n")


def print_html():
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("results.html")

    content = template.render(
        students=students,
        max_score=max_score,
        test_name=test_name
    )
    print(content)


if __name__ == "__main__":
    print_messages()
    print_html()
