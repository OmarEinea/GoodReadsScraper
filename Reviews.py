#!/usr/bin/env python

# import needed libraries
from bs4 import BeautifulSoup
from langdetect import detect
from Browser import GoodReadsBrowser
import time, os, codecs


# A class to Scrape books Reviews from GoodReads.com
class Reviews:
    def __init__(self):
        self.br = GoodReadsBrowser()
        self.ids = []
        # Counter for invalid reviews
        self.invalid = 0
        # Counter for reviews from different languages
        self.diff_lang = 0
        # Flag for indicating reviews
        # repetition due to page reload delay
        self.repeated = False
        # Write book reviews to this file
        self.file = None
        # Folder to put files in
        self.dir = "./BooksReviews/"

    # Scrape and write one book's reviews to a file
    def write_book_reviews(self, book_id):
        # Open book page by Id
        self.br.open_book(book_id)
        # Create folder if it isn't already there
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        # Open the book reviews file with utf-8 encoding
        self.file = codecs.open(self.dir + str(book_id) + ".txt", "a+", "utf-8")
        # Scrape as many reviews as possible
        while True:
            self._scrape_book(self.br.page_source)
            # Stop if there're many invalid reviews or there's no next page
            if self.invalid > 5 or self.diff_lang > 10 or not self.br.has_next_page():
                break
            # Go to next page if there's no repetition
            if not self.br.goto_next_page(self.repeated):
                self.repeated = False
            # Wait for two second for next page to load
            time.sleep(2)

    # Scrape a single page's reviews
    def _scrape_book(self, html):
        # Store reviews section of the page in soup
        soup = BeautifulSoup(html, "lxml").find(id="bookReviews")
        # Loop through reviews individually
        for review in soup.find_all(class_="bodycol"):
            # Hold rating and text part of a review
            rating = review.find(class_="staticStars")
            readable = review.find(class_="readable")
            # If one of the above is missing
            if not rating or not readable:
                # Count it as invalid
                self.invalid += 1
                continue
            # If it's not a strike of invalid reviews, reset the counter
            self.invalid = 0
            # Get full review text, even hidden parts
            comment = (readable.find(style="display:none") or readable.find()).text
            # Detect which language the review is in
            try:
                if detect(comment) != "ar":
                    raise Exception
            # Count it as a different language review
            except:
                self.diff_lang += 1
                continue
            # If it's not a strike, reset the counter
            self.diff_lang = 0
            # Hold how many stars the review was rated
            stars = str(self.SWITCH[rating.find().text])
            # Write the scraped data to the file
            self._write_review(stars, comment, readable.get("id")[19:])

    # Write data to file and prompt notification
    def _write_review(self, stars, comment, review_id):
        # If review id is already stored among ids
        if review_id in self.ids:
            # Notify and flag as repeated
            print("Repeated ID:", end=" ")
            self.repeated = True
        else:
            # Otherwise notify and store as new
            self.ids.append(review_id)
            self.file.write(stars + ' ' + comment + '\n')
            print("Added ID:", end=" ")
        print(review_id)

    # Switch reviews ratings to stars from 1 to 5
    SWITCH = {"it was amazing": 5, "really liked it": 4, "liked it": 3, "it was ok": 2, "did not like it": 1}
