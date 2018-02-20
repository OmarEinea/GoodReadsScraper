from threading import Thread
import re

id_from_url = re.compile(r"^.+/([0-9]+).*$")


class SafeThread(Thread):
    def run(self):
        try:
            Thread.run(self)
        except AttributeError:
            Thread.join(self)
            raise AttributeError


def read_books(file_name="books"):
    with open(file_name + ".txt") as file:
        books_ids = file.read().splitlines()
    return books_ids


def write_books(books_ids, file_name="books"):
    with open(file_name + ".txt", "w") as file:
        file.write("\n".join(books_ids))
