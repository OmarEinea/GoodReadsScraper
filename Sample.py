#!/usr/bin/env python

# from Books import Books
from Reviews import Reviews
from Tools import read_books
from time import sleep
# from Tools import *

if __name__ == '__main__':

    # >>> Create books object and get all books shelved as "arabic"
    # b = Books()
    # b.output_books("arabic", "shelf", file_name="books")

    # >>> Create Reviews object and scrape all reviews from the books list
    r = Reviews()
    count = 0
    while True:
        try:
            r.output_books_reviews(read_books())
            break
        # If connection is stuck, refresh reviews object
        except (AttributeError, ConnectionError, PermissionError) as e:
            print("Resetting Reviews object because:", e)
            r.stop()
            count += 1
            # Every three times this happens, wait a bit
            if count % 3 == 0:
                sleep(120)
            r.start()
        # If an error occurs
        except Exception as e:
            print("Error:", str(e))

    r.close()
    print("Done!")
    # delete_repeated_reviews()
    # combine_reviews()
    # split_reviews(5)
