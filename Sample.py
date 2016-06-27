#!/usr/bin/env python

# from Books import Books
from Reviews import Reviews
from time import sleep
# from Manager import *
if __name__ == '__main__':

    # >>> Create books object and get all books shelved as "arabic"
    # b = Books()
    # b.output_books("arabic", "shelf", file_name="books")

    # >>> Create Reviews object and scrape all reviews from the books list
    r = Reviews()
    count = 0
    while True:
        try:
            r.output_books_reviews(r.wr.read_books("books"))
            break
        # If connection is stuck, refresh reviews object
        except AttributeError as e:
            r.br.close()
            del r
            print("Refreshing Reviews Object because: " + str(e))
            count += 1
            # Every three times this happens, wait a bit
            if count % 3 == 0:
                sleep(900)
            r = Reviews()
        # If book is not found, just skip it
        except FileNotFoundError:
            pass

    # delete_repeated_reviews()
    # combine_reviews()
    # split_reviews(5)
