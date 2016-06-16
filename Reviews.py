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
        # Array for previous reviews ids
        self.ids = []
        # Counter for time of reloading a page
        self.reload = 0
        # Counter for reviews from different languages
        self.invalid = 0

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
                self.reload += 1
                if self.reload > 5:
                    print("Refreshing")
                    self.br.refresh()
                    self.reload = 0
                # Wait one second for page to load
                time.sleep(1)
                continue
            # Stop if there're many unwanted reviews or there's no next page
            if self.invalid > 20 or not self.br.has_next_page():
                break
            # Wait for two second for next page to load
            time.sleep(2)
        # Finalize file name and close it
        self.wr.close_book_file(len(self.ids))
        # Empty ids array
        self.ids = []

    # Check for possible errors then scrape book
    def _process_book(self, html):
        # Store reviews section of the page in soup
        soup = BeautifulSoup(html, "lxml").find(id="bookReviews")
        # Check if page has loaded
        if not soup:
            return False
        temp_ids = []
        reviews = []
        # Loop through reviews and their ids and store them
        for review in soup.find_all(class_="review"):
            temp_ids.append(review.get("id")[7:])
            reviews.append(review)
        # Check that no reviews are repeated
        if any(id_ in temp_ids for id_ in self.ids):
            return False
        self.ids = []
        # Invest time and go to next page from now
        if self.br.has_next_page():
            self.br.goto_next_page()
        # Good to go, start scraping book
        self._scrape_book(reviews)
        return True

    # Scrape a single page's reviews
    def _scrape_book(self, reviews):
        # Loop through reviews individually
        for review in reviews:
            try:
                # Get rating out of five stars
                stars = self.SWITCH[review.find(class_="staticStars").find().text]
                # Get full review text, even hidden parts
                comment = review.find(class_="readable").find_all("span")[-1].text
                # Detect which language the review is in
                if detect(comment) != "ar":
                    # Count it as a different language review
                    self.invalid += 1
                    continue
            # Skip the rest if one of the above is missing
            except:
                continue
            # If it's not a strike, reset the counter
            self.invalid = 0
            # Get review ID
            id_ = review.get("id")[7:]
            # Write the scraped review to the file
            self.wr.write_review(id_, stars, comment)
            # Notify and add review id to ids
            self.ids.append(id_)
            print("Added ID: " + id_)

    # Switch reviews ratings to stars from 1 to 5
    SWITCH = {"it was amazing": 5, "really liked it": 4, "liked it": 3, "it was ok": 2, "did not like it": 1}
