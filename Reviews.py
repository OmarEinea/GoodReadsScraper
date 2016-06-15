#!/usr/bin/env python

# import needed libraries
from bs4 import BeautifulSoup
from langdetect import detect
from Browser import Browser
from Writer import Writer
import time


# A class to Scrape books Reviews from GoodReads.com
class Reviews:
    def __init__(self):
        # Browsing and writing managers
        self.br = Browser()
        self.wr = Writer()
        self.ids = []
        # Counter for time of reloading a page
        self.reload = 0
        # Counter for reviews from different languages
        self.diff_lang = 0

    # Scrape and write books' reviews to separate files
    def output_books_reviews(self, books_ids, consider_previous=True):
        if consider_previous:
            # Don't loop through already scraped books
            self.wr.consider_written_files(books_ids)
        # Loop through book ids in array and scrape books
        for book_id in books_ids:
            print("Scraping book: " + book_id)
            self.output_book_reviews(book_id)

    # Scrape and write one book's reviews to a file
    def output_book_reviews(self, book_id):
        # Open book page and file by Id
        self.br.open_book_page(book_id)
        self.wr.open_book_file(book_id)
        # Scrape as many reviews as possible
        while True:
            # Scrape book page and return whether it loaded
            if not self._process_book(self.br.page_source):
                # Refresh if page didn't load for five seconds
                print("Waiting")
                if self.reload > 5:
                    print("Refreshing")
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
        # Finalize file name and close it
        self.wr.close_book_file(len(self.ids))
        # Empty ids array
        self.ids.clear()

    # Check for possible errors then scrape book
    def _process_book(self, html):
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
        # Good to go, start scraping book
        self._scrape_book(zip(soup.find_all(class_="bodycol"), temp_ids))
        return True

    # Scrape a single page's reviews
    def _scrape_book(self, reviews):
        # Loop through reviews individually
        for review, i in reviews:
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
            # Write the scraped review to the file
            self.wr.write_review(i, self.SWITCH[rating.find().text], comment)
            # Notify and add review id to ids
            self.ids.append(i)
            print("Added ID:" + i)

    # Switch reviews ratings to stars from 1 to 5
    SWITCH = {"it was amazing": 5, "really liked it": 4, "liked it": 3, "it was ok": 2, "did not like it": 1}
