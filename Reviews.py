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
        # Counter for time of reloading a page
        self.reload = 0
        # Counter for reviews from different languages
        self.diff_lang = 0
        # Write book reviews to this file
        self.file = None
        # Folder to put files in
        self.dir = "./BooksReviews/"

    # Setter for output path to write files in
    def set_output_folder(self, path):
        self.dir = path

    # Scrape and write books' reviews to separate files
    def write_books_reviews(self, books_ids, consider_previous=True):
        if consider_previous:
            # Loop through files in the chosen path
            for file in os.listdir(self.dir):
                # If file starts with digit (so not with C_ or E_)
                if file[0].isdigit():
                    # Then program was interrupted, delete file
                    os.remove(file)
                else:
                    # Otherwise, don't scrape the book again
                    books_ids.discard(file[2:-4])
        # Loop through book ids in array and scrape books
        for book_id in books_ids:
            print("Scraping book: " + book_id)
            self.write_book_reviews(book_id)

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
            # Scrape book page and return whether it loaded
            if not self._scrape_book(self.br.page_source):
                # Refresh if page didn't load for five seconds
                if self.reload > 5:
                    self.br.refresh()
                    self.reload = 0
                # Wait one second for page to load
                time.sleep(1)
                continue
            # Stop if there're many unwanted reviews or there's no next page
            if self.diff_lang > 20 or not self.br.has_next_page():
                break
            # Wait for two second for next page to load
            time.sleep(2)
        # Done writing, rename file accordingly
        self.flag_file_name(str(book_id) + ".txt")
        # Empty ids array
        self.ids.clear()

    # Scrape a single page's reviews
    def _scrape_book(self, html):
        # Store reviews section of the page in soup
        soup = BeautifulSoup(html, "lxml").find(id="bookReviews")
        # Check if page has loaded
        if not soup:
            return False
        temp_ids = []
        # Loop through reviews ids
        for review in soup.find_all(class_="review"):
            temp_ids.append(review.get("id")[7:])
        # Check that no reviews are repeated
        if any(i in temp_ids for i in self.ids[-31:]):
            return False
        # Invest time and go to next page from now
        if self.br.has_next_page():
            self.br.goto_next_page()
        # Loop through reviews individually
        for review, i in zip(soup.find_all(class_="bodycol"), temp_ids):
            # Hold rating and text part of a review
            rating = review.find(class_="staticStars")
            readable = review.find(class_="readable")
            # Skip the rest if one of the above is missing
            if not rating or not readable:
                continue
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
            # Write the scraped data to the file
            self.file.write(str(self.SWITCH[rating.find().text]) + ' ' + comment + '\n')
            # Notify and add review id to ids
            self.ids.append(i)
            print("Added ID:" + i)
        return True

    # Switch reviews ratings to stars from 1 to 5
    SWITCH = {"it was amazing": 5, "really liked it": 4, "liked it": 3, "it was ok": 2, "did not like it": 1}

    # Rename done files to complete or empty
    def flag_file_name(self, name):
        # If no reviews were added
        if len(self.ids) == 0:
            # Rename as an empty file
            os.rename(self.dir + name, self.dir + "E_" + name)
        else:
            # Otherwise, rename as a complete file
            os.rename(self.dir + name, self.dir + "C_" + name)
