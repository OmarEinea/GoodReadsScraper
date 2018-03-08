#!/usr/bin/env python

from Books import Books
from Reviews import Reviews
from Tools import read_books
from time import sleep
# from Tools import *

if __name__ == '__main__':

    # >>> Create books object and get all books shelved as "arabic"
    b = Books(arabic=False)
    # b.append_books(read_books())
    b.output_books(2522)
    while not b.output_books_editions(read_books(), file_name="editions"):
        print("Refreshing after a while")
        sleep(50)
    while not b.output_books_edition_by_language(read_books("editions"), file_name="ara_books"):
        print("Refreshing after a while")
        sleep(50)
    # >>> Create Reviews object and scrape all reviews from the books list
    r = Reviews(edition_reviews=True)
    while True:
        try:
            r.output_books_reviews(read_books("ara_books_list"))
            break
        # If an error occurs
        except Exception as e:
            print("ERROR:", str(e))
            r.reset()
    r.close()
    print("Done!")
    # delete_repeated_reviews()
    # combine_reviews()
    # split_reviews(5)
